"""Cross-platform synchronization for marketplace listings and inventory management."""
from typing import Dict, Any, Optional, List, Tuple
import logging
from datetime import datetime
import asyncio
from decimal import Decimal

from .base import MarketplaceClient
from .ebay_client import EbayClient
from .exceptions import MarketplaceError
from ..db import get_db

logger = logging.getLogger(__name__)

class CrossPlatformSync:
    """Handles synchronization of listings across multiple marketplaces."""

    def __init__(self):
        """Initialize cross-platform sync service."""
        self.marketplace_clients: Dict[str, MarketplaceClient] = {
            "ebay": EbayClient(
                client_id="development-id",
                client_secret="development-secret"
            )
            # Future marketplace clients will be added here:
            # "amazon": AmazonClient(...),
            # "etsy": EtsyClient(...)
        }
        self.db = get_db()
        
    async def allocate_inventory(
        self,
        total_stock: int,
        marketplaces: List[str]
    ) -> Dict[str, int]:
        """
        Allocate inventory across marketplaces based on performance metrics.
        
        Args:
            total_stock: Total available stock
            marketplaces: List of marketplaces to allocate stock to
            
        Returns:
            Dictionary mapping marketplace to allocated stock
        """
        if not marketplaces:
            return {}
            
        try:
            db = await self.db
            
            # Get marketplace performance metrics
            performance_data = {}
            for marketplace in marketplaces:
                # Calculate success rate and average sale time
                listings = await db.listing.find_many(
                    where={
                        'marketplace': marketplace,
                        'orders': {
                            'some': {}
                        }
                    },
                    include={
                        'orders': True
                    }
                )
                
                if not listings:
                    performance_data[marketplace] = {
                        'weight': 1.0  # Default weight for new marketplaces
                    }
                    continue
                
                total_orders = 0
                successful_orders = 0
                total_time = 0
                
                for listing in listings:
                    listing_orders = [
                        order for order in listing.orders
                        if order.status in ('completed', 'cancelled')
                    ]
                    
                    total_orders += len(listing_orders)
                    successful_orders += sum(
                        1 for order in listing_orders
                        if order.status == 'completed'
                    )
                    
                    # Calculate average time to sell
                    for order in listing_orders:
                        if order.status == 'completed':
                            time_to_sell = (
                                order.completedAt - listing.createdAt
                            ).total_seconds() / 3600  # Convert to hours
                            total_time += time_to_sell
                
                success_rate = (
                    successful_orders / total_orders
                    if total_orders > 0 else 0.5
                )
                avg_time = (
                    total_time / successful_orders
                    if successful_orders > 0 else 168  # Default 1 week
                )
                
                # Calculate weight based on success rate and speed
                time_factor = 168 / (avg_time + 168)  # Normalize time factor
                weight = success_rate * 0.7 + time_factor * 0.3
                
                performance_data[marketplace] = {
                    'weight': max(0.1, weight)  # Minimum weight of 0.1
                }
            
            # Allocate stock based on weights
            total_weight = sum(data['weight'] for data in performance_data.values())
            base_allocations = {
                marketplace: max(1, int(total_stock * data['weight'] / total_weight))
                for marketplace, data in performance_data.items()
            }
            
            
            # Distribute remaining stock
            allocated = sum(base_allocations.values())
            remaining = total_stock - allocated
            
            if remaining > 0:
                # Sort marketplaces by weight for remaining allocation
                sorted_marketplaces = sorted(
                    marketplaces,
                    key=lambda m: performance_data[m]['weight'],
                    reverse=True
                )
                
                for i in range(remaining):
                    base_allocations[sorted_marketplaces[i % len(sorted_marketplaces)]] += 1
            
            return base_allocations
            
        except Exception as e:
            logger.error(f"Error allocating inventory: {str(e)}")
            # Fall back to even distribution
            base_amount = total_stock // len(marketplaces)
            remainder = total_stock % len(marketplaces)
            
            return {
                marketplace: base_amount + (1 if i < remainder else 0)
                for i, marketplace in enumerate(marketplaces)
            }

    async def sync_inventory_levels(
        self,
        item_id: str,
        total_stock: int
    ) -> Dict[str, Any]:
        """
        Synchronize inventory levels across all marketplaces.
        
        Args:
            item_id: ID of the item to sync
            total_stock: Total available stock
            
        Returns:
            Dictionary containing sync results
        """
        try:
            db = await self.db
            
            # Get all active listings for this item
            listings = await db.listing.find_many(
                where={
                    'itemId': item_id,
                    'status': 'active'
                }
            )
            
            if not listings:
                return {
                    'status': 'no_active_listings',
                    'item_id': item_id
                }
            
            # Get unique marketplaces
            active_marketplaces = list(set(
                listing.marketplace for listing in listings
            ))
            
            # Allocate inventory across marketplaces
            allocations = await self.allocate_inventory(
                total_stock,
                active_marketplaces
            )
            
            results = {}
            update_tasks = []
            
            for marketplace, allocated_stock in allocations.items():
                marketplace_listings = [
                    l for l in listings
                    if l.marketplace == marketplace
                ]
                
                for listing in marketplace_listings:
                    if allocated_stock == 0:
                        # Delist if no stock allocated
                        update_tasks.append(
                            self.delist_item(listing.id, marketplace)
                        )
                        results[listing.id] = {
                            'action': 'delisted',
                            'reason': 'no_stock'
                        }
                    else:
                        # Update stock level
                        update_tasks.append(
                            self.update_listing_stock(
                                listing.id,
                                allocated_stock,
                                marketplace
                            )
                        )
                        results[listing.id] = {
                            'action': 'updated',
                            'new_stock': allocated_stock
                        }
            
            # Execute all updates concurrently
            await asyncio.gather(*update_tasks)
            
            return {
                'status': 'success',
                'item_id': item_id,
                'total_stock': total_stock,
                'allocations': allocations,
                'listing_results': results
            }
            
        except Exception as e:
            logger.error(f"Error syncing inventory levels: {str(e)}")
            raise
            
    async def create_or_update_listing(
        self,
        listing_data: Dict[str, Any],
        marketplaces: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create or update a listing across specified marketplaces.
        
        Args:
            listing_data: Dictionary containing listing details
            marketplaces: List of marketplace names to sync with (default: all)
        
        Returns:
            Dictionary containing status and platform-specific responses
        
        Raises:
            MarketplaceError: If listing creation/update fails
        """
        results = {}
        target_marketplaces = marketplaces or list(self.marketplace_clients.keys())

        for marketplace in target_marketplaces:
            try:
                if client := self.marketplace_clients.get(marketplace):
                    # Add marketplace-specific data
                    platform_data = {
                        **listing_data,
                        "marketplace": marketplace,
                        "sync_timestamp": datetime.now().isoformat()
                    }
                    
                    # Create/update listing on platform
                    response = await client.create_listing(platform_data)
                    
                    results[marketplace] = {
                        "status": "success",
                        "external_id": response.get("external_id"),
                        "url": response.get("url"),
                        "timestamp": platform_data["sync_timestamp"]
                    }
                else:
                    results[marketplace] = {
                        "status": "error",
                        "error": f"Unsupported marketplace: {marketplace}"
                    }
            except MarketplaceError as e:
                logger.error(f"Failed to sync listing with {marketplace}: {str(e)}")
                results[marketplace] = {
                    "status": "error",
                    "error": str(e)
                }
            except Exception as e:
                logger.error(f"Unexpected error syncing with {marketplace}: {str(e)}")
                results[marketplace] = {
                    "status": "error",
                    "error": f"Unexpected error: {str(e)}"
                }

        return {
            "status": "completed",
            "platform_results": results,
            "sync_timestamp": datetime.now().isoformat()
        }

    async def update_listing_stock(
        self,
        listing_id: str,
        quantity: int,
        marketplace: str
    ) -> None:
        """
        Update stock level for a specific listing.
        
        Args:
            listing_id: ID of the listing to update
            quantity: New stock quantity
            marketplace: Marketplace name
        """
        try:
            if client := self.marketplace_clients.get(marketplace):
                await client.update_stock(listing_id, quantity)
                
                # Update database
                db = await self.db
                await db.listing.update(
                    where={'id': listing_id},
                    data={
                        'quantity': quantity,
                        'lastStockUpdate': datetime.now()
                    }
                )
            else:
                raise MarketplaceError(f"Unsupported marketplace: {marketplace}")
                
        except Exception as e:
            logger.error(
                f"Error updating stock for listing {listing_id} "
                f"on {marketplace}: {str(e)}"
            )
            raise
            
    async def delist_item(
        self,
        listing_id: str,
        marketplace: str
    ) -> None:
        """
        Remove listing from marketplace.
        
        Args:
            listing_id: ID of the listing to remove
            marketplace: Marketplace name
        """
        try:
            if client := self.marketplace_clients.get(marketplace):
                await client.end_listing(listing_id)
                
                # Update database
                db = await self.db
                await db.listing.update(
                    where={'id': listing_id},
                    data={
                        'status': 'ended',
                        'endedAt': datetime.now()
                    }
                )
            else:
                raise MarketplaceError(f"Unsupported marketplace: {marketplace}")
                
        except Exception as e:
            logger.error(
                f"Error delisting item {listing_id} "
                f"from {marketplace}: {str(e)}"
            )
            raise
            
    async def get_platform_status(self, marketplace: str) -> Dict[str, Any]:
        """Get platform connection status and capabilities.
        
        Args:
            marketplace: Name of the marketplace
        
        Returns:
            Dictionary containing platform status information
        """
        if client := self.marketplace_clients.get(marketplace):
            try:
                # Basic authentication check
                await client.authenticate()
                return {
                    "platform": marketplace,
                    "status": "connected",
                    "capabilities": [
                        "create_listing",
                        "market_research",
                        "price_history"
                    ]
                }
            except Exception as e:
                return {
                    "platform": marketplace,
                    "status": "error",
                    "error": str(e)
                }
        return {
            "platform": marketplace,
            "status": "unsupported"
        }
