from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from ...db import get_db

class AnalyticsService:
    async def calculate_performance_metrics(self, listing_id: str) -> Dict[str, Any]:
        """
        Calculate performance metrics for a specific listing
        
        Args:
            listing_id: The ID of the listing to analyze
            
        Returns:
            Dict containing performance metrics including:
            - view_count: Total views
            - click_count: Total clicks
            - conversion_rate: Percentage of views that led to clicks
            - revenue: Total revenue generated
            - profit_margin: Average profit margin
            - platform_performance: Platform-specific metrics
        """
        try:
            # Fetch analytics data for the listing
            async for db in get_db():
                analytics_data = await db.analyticsdata.find_first(
                    where={
                        "listing_id": listing_id
                    }
                )
            
            if not analytics_data:
                return {
                    "error": "No analytics data found for listing",
                    "listing_id": listing_id,
                    "view_count": 0,
                    "click_count": 0,
                    "conversion_rate": 0.0,
                    "revenue": 0.0,
                    "profit_margin": 0.0,
                    "platform_performance": {}
                }
            
            # Calculate conversion rate
            conversion_rate = (
                (analytics_data.click_count / analytics_data.view_count * 100)
                if analytics_data.view_count > 0
                else 0.0
            )
            
            # Format response
            return {
                "listing_id": listing_id,
                "view_count": analytics_data.view_count,
                "click_count": analytics_data.click_count,
                "conversion_rate": round(conversion_rate, 2),
                "revenue": float(analytics_data.revenue),
                "profit_margin": analytics_data.profit_margin or 0.0,
                "platform_performance": analytics_data.platform_metrics or {}
            }
            
        except Exception as e:
            # Log error and return error response
            print(f"Error calculating performance metrics: {str(e)}")
            return {
                "error": "Failed to calculate performance metrics",
                "listing_id": listing_id,
                "message": str(e)
            }
    
    async def update_analytics_data(
        self,
        listing_id: str,
        view_count: Optional[int] = None,
        click_count: Optional[int] = None,
        revenue: Optional[float] = None,
        profit_margin: Optional[float] = None,
        platform_metrics: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Update analytics data for a listing
        
        Args:
            listing_id: The ID of the listing to update
            view_count: Number of views to add
            click_count: Number of clicks to add
            revenue: Revenue to add
            profit_margin: New profit margin
            platform_metrics: Platform-specific metrics to update
            
        Returns:
            Updated analytics data
        """
        try:
            # Get existing analytics data or create new
            async for db in get_db():
                analytics_data = await db.analyticsdata.upsert(
                    where={
                        "listing_id": listing_id
                    },
                data={
                    "create": {
                        "listing_id": listing_id,
                        "view_count": view_count or 0,
                        "click_count": click_count or 0,
                        "revenue": revenue or 0.0,
                        "profit_margin": profit_margin,
                        "platform_metrics": platform_metrics or {}
                    },
                    "update": {
                        "view_count": {"increment": view_count} if view_count else None,
                        "click_count": {"increment": click_count} if click_count else None,
                        "revenue": {"increment": revenue} if revenue else None,
                        "profit_margin": profit_margin if profit_margin is not None else None,
                        "platform_metrics": platform_metrics if platform_metrics else None
                    }
                }
            )
            
            return {
                "success": True,
                "analytics_data": analytics_data
            }
            
        except Exception as e:
            print(f"Error updating analytics data: {str(e)}")
            return {
                "error": "Failed to update analytics data",
                "listing_id": listing_id,
                "message": str(e)
            }
            
    async def get_analytics_data_range(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Get analytics data for all listings within a date range.
        
        Args:
            start_date: Start of the date range
            end_date: End of the date range
            
        Returns:
            List of analytics data entries within the date range
        """
        try:
            async for db in get_db():
                analytics_data = await db.analyticsdata.find_many(
                where={
                    "updated_at": {
                        "gte": start_date,
                        "lte": end_date
                    }
                }
            )
            
            return [data.dict() for data in analytics_data]
            
        except Exception as e:
            print(f"Error fetching analytics data range: {str(e)}")
            return []
            
    async def create_analytics_snapshot(
        self,
        timestamp: datetime,
        metrics: Dict[str, Any]
    ) -> None:
        """
        Create a new analytics snapshot with aggregated metrics.
        
        Args:
            timestamp: Timestamp for the snapshot
            metrics: Aggregated metrics to store
        """
        try:
            async for db in get_db():
                await db.analyticssnapshot.create(
                data={
                    "timestamp": timestamp,
                    "metrics": metrics
                }
            )
        except Exception as e:
            print(f"Error creating analytics snapshot: {str(e)}")
            raise
