"""
FastAPI router for listing generation endpoints.

This module provides endpoints for generating optimized listing content
and managing cross-platform listing creation.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from ..services.listing_generation.listing_generator import ListingGenerator, ListingDetails
from ..marketplace_integrations.base import MarketplaceClient
from ..marketplace_integrations.ebay_client import EbayClient

router = APIRouter(prefix="/api/listings", tags=["listings"])

class ListingRequest(BaseModel):
    """Request model for listing generation."""
    title: str = Field(..., min_length=3, max_length=80)
    brand: Optional[str] = Field(None, max_length=50)
    condition: str = Field(..., 
        description="Item condition (e.g., 'New', 'Used - Like New', 'Used - Good')")
    category: Optional[str] = None
    description: Optional[str] = None
    marketplace: Optional[str] = Field("ebay", description="Target marketplace platform")

class ListingResponse(BaseModel):
    """Response model for generated listing details."""
    optimized_title: str
    optimized_description: str
    tags: List[str]
    seo_score: Optional[float] = None
    keyword_density: Optional[Dict[str, float]] = None
    marketplace_specific: Optional[Dict] = None

async def get_listing_generator() -> ListingGenerator:
    """Dependency injection for ListingGenerator service."""
    # TODO: Initialize with actual NLP and SEO services
    return ListingGenerator(
        nlp_model=None,  # Placeholder for NLP model
        seo_service=None  # Placeholder for SEO service
    )

async def get_marketplace_client(marketplace: Optional[str] = "ebay") -> MarketplaceClient:
    """Dependency injection for marketplace client."""
    marketplace = marketplace or "ebay"  # Handle None case
    if marketplace.lower() == "ebay":
        # TODO: Get these from environment variables
        return EbayClient(
            client_id="development-id",
            client_secret="development-secret"
        )
    raise HTTPException(
        status_code=400,
        detail=f"Unsupported marketplace: {marketplace}"
    )

@router.post("/generate", response_model=ListingResponse)
async def generate_listing(
    listing_req: ListingRequest,
    generator: ListingGenerator = Depends(get_listing_generator)
) -> ListingResponse:
    """Generate optimized listing content.
    
    Args:
        listing_req: Listing generation request containing item details
        generator: Injected ListingGenerator service
    
    Returns:
        ListingResponse containing optimized listing content
    
    Raises:
        HTTPException: If listing generation fails
    """
    try:
        result: ListingDetails = generator.generate_listing_details(listing_req.dict())
        
        return ListingResponse(
            optimized_title=result.title,
            optimized_description=result.description,
            tags=result.tags,
            seo_score=result.seo_score,
            keyword_density=result.keyword_density
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate listing")

@router.post("/create", response_model=ListingResponse)
async def create_platform_listing(
    listing_req: ListingRequest,
    generator: ListingGenerator = Depends(get_listing_generator)
) -> ListingResponse:
    """Create listing on specified marketplace platform.
    
    Args:
        listing_req: Listing creation request containing item details
        generator: Injected ListingGenerator service
    
    Returns:
        ListingResponse containing created listing details
    
    Raises:
        HTTPException: If listing creation fails
    """
    try:
        # Generate optimized content
        listing_details: ListingDetails = generator.generate_listing_details(
            listing_req.dict()
        )
        
        # Get marketplace client
        marketplace_client = await get_marketplace_client(listing_req.marketplace)
        
        # Create listing on marketplace
        marketplace_response = await marketplace_client.create_listing({
            "title": listing_details.title,
            "description": listing_details.description,
            "tags": listing_details.tags,
            **listing_req.dict()
        })
        
        return ListingResponse(
            optimized_title=listing_details.title,
            optimized_description=listing_details.description,
            tags=listing_details.tags,
            seo_score=listing_details.seo_score,
            keyword_density=listing_details.keyword_density,
            marketplace_specific=marketplace_response
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create listing: {str(e)}"
        )
