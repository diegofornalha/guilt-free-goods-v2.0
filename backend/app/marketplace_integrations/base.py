"""Base classes for marketplace integrations."""
from abc import ABC, abstractmethod
from typing import Dict, Any

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
