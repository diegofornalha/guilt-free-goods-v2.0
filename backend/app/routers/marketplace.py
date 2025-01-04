"""
FastAPI router for marketplace integration endpoints.

This module provides API endpoints for interacting with various marketplace
integrations (eBay, Amazon, Etsy, etc.) for market research and pricing data.
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..marketplace_integrations.ebay_client import EbayClient
from ..marketplace_integrations.exceptions import (
    AuthenticationError,
    MarketDataError,
    ParseError,
    HistoricalDataError,
)

router = APIRouter(prefix="/api/marketplace", tags=["marketplace"])

class MarketDataResponse(BaseModel):
    """Response model for market data endpoints."""
    marketplace: str
    item_id: str
    results: Dict[str, Any]

@router.get("/fetch-data", response_model=MarketDataResponse)
async def fetch_market_data(
    marketplace: str = Query(..., description="Marketplace to fetch data from (e.g., ebay)"),
    item_id: str = Query(..., description="Item identifier to search for"),
) -> MarketDataResponse:
    """
    Fetch market data for a specific item from the specified marketplace.

    Args:
        marketplace: Name of the marketplace (e.g., ebay)
        item_id: Item identifier to search for

    Returns:
        MarketDataResponse containing the parsed market data

    Raises:
        HTTPException: If the marketplace is not supported or if an error occurs
    """
    try:
        if marketplace.lower() != "ebay":
            raise HTTPException(
                status_code=400,
                detail=f"Marketplace '{marketplace}' is not supported. Currently only 'ebay' is supported."
            )

        # Initialize client with development credentials
        # TODO: Load credentials from environment variables
        client = EbayClient(client_id="development", client_secret="development")
        
        # Authenticate with the marketplace
        client.authenticate()
        
        # Fetch and parse market data
        raw_data = client.fetch_market_data(item_id)
        parsed_data = client.parse_response(raw_data)
        
        return MarketDataResponse(
            marketplace=marketplace,
            item_id=item_id,
            results=parsed_data
        )
        
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except MarketDataError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except ParseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/price-history", response_model=MarketDataResponse)
async def get_price_history(
    marketplace: str = Query(..., description="Marketplace to fetch history from (e.g., ebay)"),
    item_id: str = Query(..., description="Item identifier to search for"),
    days: Optional[int] = Query(30, description="Number of days of history to fetch", ge=1, le=365),
) -> MarketDataResponse:
    """
    Fetch price history for a specific item from the specified marketplace.

    Args:
        marketplace: Name of the marketplace (e.g., ebay)
        item_id: Item identifier to search for
        days: Number of days of history to fetch (default: 30, max: 365)

    Returns:
        MarketDataResponse containing the historical price data

    Raises:
        HTTPException: If the marketplace is not supported or if an error occurs
    """
    try:
        if marketplace.lower() != "ebay":
            raise HTTPException(
                status_code=400,
                detail=f"Marketplace '{marketplace}' is not supported. Currently only 'ebay' is supported."
            )

        # Initialize client with development credentials
        # TODO: Load credentials from environment variables
        client = EbayClient(client_id="development", client_secret="development")
        
        # Authenticate with the marketplace
        client.authenticate()
        
        # Fetch historical data
        history_data = client.get_price_history(item_id, days)
        
        return MarketDataResponse(
            marketplace=marketplace,
            item_id=item_id,
            results=history_data
        )
        
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except HistoricalDataError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
