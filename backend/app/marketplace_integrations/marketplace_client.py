"""
Base class for marketplace integrations providing a common interface for all marketplace clients.

This abstract class defines the required methods that all marketplace clients must implement
to ensure consistent behavior across different marketplace integrations (eBay, Amazon, Etsy, etc.).
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class MarketplaceClient(ABC):
    """Abstract base class for marketplace API clients."""

    @abstractmethod
    def authenticate(self, *args: Any, **kwargs: Any) -> None:
        """
        Authenticate with the marketplace API.

        Args:
            *args: Variable length argument list for authentication parameters
            **kwargs: Arbitrary keyword arguments for authentication parameters

        Raises:
            AuthenticationError: If authentication fails
        """
        pass

    @abstractmethod
    def fetch_market_data(self, item_identifier: str) -> Dict[str, Any]:
        """
        Fetch market data for a specific item.

        Args:
            item_identifier: Unique identifier for the item (e.g., SKU, UPC, model number)

        Returns:
            Dict containing market data (prices, listings, etc.)

        Raises:
            MarketDataError: If fetching market data fails
        """
        pass

    @abstractmethod
    def parse_response(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the raw API response into a standardized format.

        Args:
            response_data: Raw API response data

        Returns:
            Dict containing parsed and standardized market data

        Raises:
            ParseError: If parsing the response fails
        """
        pass

    @abstractmethod
    def get_price_history(
        self, item_identifier: str, days: Optional[int] = 30
    ) -> Dict[str, Any]:
        """
        Fetch historical price data for an item.

        Args:
            item_identifier: Unique identifier for the item
            days: Number of days of history to fetch (default: 30)

        Returns:
            Dict containing historical price data

        Raises:
            HistoricalDataError: If fetching historical data fails
        """
        pass
