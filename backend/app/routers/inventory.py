"""Inventory management router."""
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException

from ..db import get_db
from ..marketplace_integrations.cross_platform_sync import CrossPlatformSync

router = APIRouter(prefix="/inventory", tags=["inventory"])
sync_service = CrossPlatformSync()

@router.put("/{item_id}/stock")
async def update_stock_level(
    item_id: str,
    total_stock: int,
    db=Depends(get_db)
) -> Dict[str, Any]:
    """Update stock level for an item across all marketplaces.
    
    Args:
        item_id: ID of the item to update
        total_stock: New total stock quantity
        
    Returns:
        Dictionary containing sync results
    """
    try:
        # Verify item exists
        item = await db.item.find_unique(
            where={'id': item_id},
            include={
                'listings': {
                    'where': {
                        'status': 'active'
                    }
                }
            }
        )
        
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f"Item {item_id} not found"
            )
            
        # Sync stock across marketplaces
        sync_result = await sync_service.sync_inventory_levels(
            item_id,
            total_stock
        )
        
        # Update master inventory
        await db.item.update(
            where={'id': item_id},
            data={
                'stockQuantity': total_stock,
                'lastStockUpdate': datetime.now()
            }
        )
        
        return {
            'status': 'success',
            'item_id': item_id,
            'total_stock': total_stock,
            'sync_results': sync_result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update stock: {str(e)}"
        )

@router.get("/{item_id}/stock")
async def get_stock_level(
    item_id: str,
    db=Depends(get_db)
) -> Dict[str, Any]:
    """Get current stock level for an item.
    
    Args:
        item_id: ID of the item to check
        
    Returns:
        Dictionary containing stock information
    """
    try:
        item = await db.item.find_unique(
            where={'id': item_id},
            include={
                'listings': {
                    'where': {
                        'status': 'active'
                    }
                }
            }
        )
        
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f"Item {item_id} not found"
            )
            
        # Get stock levels from each marketplace
        marketplace_stock = {}
        for listing in item.listings:
            try:
                if client := sync_service.marketplace_clients.get(listing.marketplace):
                    stock = await client.get_stock_level(listing.id)
                    marketplace_stock[listing.marketplace] = stock
            except Exception as e:
                marketplace_stock[listing.marketplace] = {
                    'error': str(e)
                }
                
        return {
            'item_id': item_id,
            'total_stock': item.stockQuantity,
            'marketplace_stock': marketplace_stock,
            'last_update': item.lastStockUpdate
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stock level: {str(e)}"
        )
