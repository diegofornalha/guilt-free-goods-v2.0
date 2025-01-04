"""Custom exceptions for marketplace integrations."""

class MarketplaceError(Exception):
    """Base exception for marketplace-related errors."""
    pass

class AuthenticationError(MarketplaceError):
    """Raised when authentication with a marketplace API fails."""
    pass

class MarketDataError(MarketplaceError):
    """Raised when fetching market data fails."""
    pass

class ParseError(MarketplaceError):
    """Raised when parsing marketplace API response fails."""
    pass

class HistoricalDataError(MarketplaceError):
    """Raised when fetching historical data fails."""
    pass
