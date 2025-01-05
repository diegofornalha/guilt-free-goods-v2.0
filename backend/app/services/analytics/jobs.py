"""
Background jobs for analytics data aggregation and snapshot generation.

This module implements scheduled jobs that periodically aggregate analytics data
and generate daily snapshots for trend analysis.
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

from ...db import get_db
from .analytics_service import AnalyticsService

logger = logging.getLogger(__name__)

async def generate_daily_snapshot() -> None:
    """
    Generate a daily analytics snapshot by aggregating data across all listings.
    
    This job:
    1. Aggregates analytics data from the past 24 hours
    2. Calculates key performance metrics
    3. Stores the snapshot in the database
    """
    try:
        analytics_service = AnalyticsService()
        current_time = datetime.utcnow()
        yesterday = current_time - timedelta(days=1)
        
        # Get database connection and aggregate metrics across all listings
        aggregated_metrics = {
            "price_accuracy": 0.0,
            "data_freshness": 0.0,
            "coverage_rate": 0.0,
            "total_listings": 0,
            "active_listings": 0,
            "total_views": 0,
            "total_sales": 0,
            "average_price": 0.0
        }
        
        # Get all analytics data from the past 24 hours
        analytics_data = await analytics_service.get_analytics_data_range(
            start_date=yesterday,
            end_date=current_time
        )
        
        if not analytics_data:
            logger.warning("No analytics data found for snapshot generation")
            return
            
        # Process analytics data
            # Calculate averages and totals
            total_listings = len(analytics_data)
            for data in analytics_data:
                metrics = data.get("metrics", {})
                aggregated_metrics["price_accuracy"] += metrics.get("price_accuracy", 0)
                aggregated_metrics["data_freshness"] += metrics.get("data_freshness", 0)
                aggregated_metrics["coverage_rate"] += metrics.get("coverage_rate", 0)
                aggregated_metrics["total_views"] += data.get("views", 0)
                aggregated_metrics["total_sales"] += data.get("sales", 0)
                
                if data.get("status") == "active":
                    aggregated_metrics["active_listings"] += 1
                    
                price = data.get("market_data", {}).get("current_data", {}).get("price", 0)
                if price > 0:
                    aggregated_metrics["average_price"] += price
            
            # Calculate final averages
            aggregated_metrics["price_accuracy"] /= total_listings
            aggregated_metrics["data_freshness"] /= total_listings
            aggregated_metrics["coverage_rate"] /= total_listings
            aggregated_metrics["average_price"] /= aggregated_metrics["active_listings"] or 1
            aggregated_metrics["total_listings"] = total_listings
            
            # Store the snapshot
            await analytics_service.create_analytics_snapshot(
                timestamp=current_time,
                metrics=aggregated_metrics
            )
            
            logger.info(f"Generated daily analytics snapshot: {aggregated_metrics}")
            
        else:
            logger.warning("No analytics data found for snapshot generation")
            
    except Exception as e:
        logger.error(f"Failed to generate daily analytics snapshot: {str(e)}")
        raise

async def schedule_daily_snapshot(hour: int = 0, minute: int = 0) -> None:
    """
    Schedule the daily snapshot generation to run at a specific time.
    
    Args:
        hour: Hour of the day to run (0-23)
        minute: Minute of the hour to run (0-59)
    """
    while True:
        try:
            now = datetime.utcnow()
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if next_run <= now:
                next_run += timedelta(days=1)
                
            # Sleep until next scheduled run
            sleep_seconds = (next_run - now).total_seconds()
            logger.info(f"Scheduling next snapshot for {next_run} (in {sleep_seconds} seconds)")
            await asyncio.sleep(sleep_seconds)
            
            # Generate the snapshot
            await generate_daily_snapshot()
            
        except Exception as e:
            logger.error(f"Error in snapshot scheduler: {str(e)}")
            # Sleep for a minute before retrying
            await asyncio.sleep(60)
