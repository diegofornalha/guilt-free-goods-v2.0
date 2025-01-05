from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from ..services.analytics.analytics_service import AnalyticsService
from ..db import get_db, db

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/performance/{listing_id}")
async def get_listing_performance(
    listing_id: str,
    db = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get performance metrics for a specific listing.
    
    Args:
        listing_id: The ID of the listing to get metrics for
        db: Database connection from dependency injection
    
    Returns:
        Dict containing performance metrics for the listing
    
    Raises:
        HTTPException: If listing is not found or other errors occur
    """
    try:
        analytics_service = AnalyticsService()
        metrics = await analytics_service.calculate_performance_metrics(listing_id)
        return metrics
    except Exception as e:
        raise HTTPException(
            status_code=404 if "not found" in str(e).lower() else 500,
            detail=str(e)
        )

@router.get("/summary")
async def get_analytics_summary(
    db = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get a summary of overall platform analytics.
    
    Args:
        db: Database connection from dependency injection
    
    Returns:
        Dict containing summary analytics data
    
    Raises:
        HTTPException: If there's an error retrieving analytics data
    """
    try:
        analytics_service = AnalyticsService()
        # TODO: Implement summary calculation in analytics service
        return {
            "status": "Not implemented",
            "message": "Analytics summary endpoint is under development"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
