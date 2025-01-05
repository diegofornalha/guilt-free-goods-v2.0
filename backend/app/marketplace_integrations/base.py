"""Base classes for marketplace integrations."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class MarketplaceClient(ABC):
    """Abstract base class for marketplace clients."""
    
    @abstractmethod
    async def create_listing(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a listing on the marketplace platform.
        
        Args:
            listing_data: Dictionary containing listing details
        
        Returns:
            Dictionary containing marketplace-specific response data
        
        Raises:
            MarketplaceError: If listing creation fails
        """
        pass
        
    @abstractmethod
    async def update_stock(self, listing_id: str, quantity: int) -> None:
        """Update stock level for a listing.
        
        Args:
            listing_id: ID of the listing to update
            quantity: New stock quantity
            
        Raises:
            MarketplaceError: If stock update fails
        """
        pass
        
    @abstractmethod
    async def end_listing(self, listing_id: str) -> None:
        """End/remove a listing from the marketplace.
        
        Args:
            listing_id: ID of the listing to end
            
        Raises:
            MarketplaceError: If ending the listing fails
        """
        pass
        
    @abstractmethod
    async def get_stock_level(self, listing_id: str) -> Optional[int]:
        """Get current stock level for a listing.
        
        Args:
            listing_id: ID of the listing to check
            
        Returns:
            Current stock quantity or None if listing not found
            
        Raises:
            MarketplaceError: If fetching stock level fails
        """
        pass
