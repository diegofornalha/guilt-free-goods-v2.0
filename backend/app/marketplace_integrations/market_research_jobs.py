"""
Background jobs for marketplace research and pricing data collection.

This module implements scheduled jobs that periodically fetch and store
pricing data from various marketplaces for trend analysis and analytics updates.
It also provides advanced market analysis features including:
- Historical price trend analysis
- Seasonal demand prediction
- Competitive pricing analysis across marketplaces
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import numpy as np
from collections import defaultdict

from .ebay_client import EbayClient
from .exceptions import MarketDataError, AuthenticationError
from ..services.analytics.analytics_service import AnalyticsService
from ..db import get_db

logger = logging.getLogger(__name__)

class MarketResearchJob:
    """Handles periodic market research data collection and analysis."""
    
    def __init__(self):
        # TODO: Load from environment variables
        self.ebay_client = EbayClient(
            client_id="development",
            client_secret="development"
        )
        self.db = get_db()
        self.analytics_service = AnalyticsService()
        
    async def collect_market_data(
        self,
        item_ids: List[str],
        days_history: Optional[int] = 30
    ) -> Dict[str, Any]:
        """
        Collect market data for specified items.
        
        Args:
            item_ids: List of item identifiers to research
            days_history: Number of days of price history to collect
            
        Returns:
            Dictionary containing collected market data
        """
        try:
            await self.ebay_client.authenticate()
            
            results = {}
            for item_id in item_ids:
                try:
                    # Fetch current market data
                    current_data = await self.ebay_client.fetch_market_data(item_id)
                    parsed_data = self.ebay_client.parse_response(current_data)
                    
                    # Fetch historical data if requested
                    if days_history:
                        history_data = await self.ebay_client.get_price_history(
                            item_id,
                            days=days_history
                        )
                    else:
                        history_data = None
                    
                    results[item_id] = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "current_data": parsed_data,
                        "price_history": history_data
                    }
                    
                except (MarketDataError, AuthenticationError) as e:
                    logger.error(f"Error collecting data for item {item_id}: {str(e)}")
                    results[item_id] = {
                        "timestamp": datetime.utcnow().isoformat(),
                        "error": str(e)
                    }
                    
            return results
            
        except Exception as e:
            logger.error(f"Market research job failed: {str(e)}")
            raise

    async def analyze_historical_prices(self, item_id: str) -> Dict[str, Any]:
        """
        Analyze historical price trends for an item.
        
        Args:
            item_id: The ID of the item to analyze
            
        Returns:
            Dictionary containing price trend analysis
        """
        try:
            # Get all listings for this item
            listings = await self.db.listing.find_many(
                where={'itemId': item_id},
                include={
                    'marketResearch': True,
                    'orders': True
                }
            )
            
            if not listings:
                return {
                    'trend': 'insufficient_data',
                    'average_price': None,
                    'price_range': None,
                    'confidence': 0.0
                }
            
            # Collect price data points
            price_data = []
            for listing in listings:
                # Add listing price
                price_data.append({
                    'price': float(listing.price),
                    'date': listing.createdAt,
                    'type': 'listing'
                })
                
                # Add successful order prices
                for order in listing.orders:
                    if order.status == 'completed':
                        price_data.append({
                            'price': float(order.totalPrice),
                            'date': order.createdAt,
                            'type': 'sale'
                        })
            
            # Sort by date
            price_data.sort(key=lambda x: x['date'])
            
            # Calculate trends
            if len(price_data) < 2:
                trend = 'insufficient_data'
                confidence = 0.0
            else:
                prices = [p['price'] for p in price_data]
                dates = [(p['date'] - price_data[0]['date']).days for p in price_data]
                
                # Simple linear regression for trend
                coeffs = np.polyfit(dates, prices, 1)
                trend = 'increasing' if coeffs[0] > 0.01 else \
                       'decreasing' if coeffs[0] < -0.01 else 'stable'
                
                
                # Calculate R-squared for confidence
                y_pred = np.polyval(coeffs, dates)
                ss_tot = sum((p - np.mean(prices))**2 for p in prices)
                ss_res = sum((prices[i] - y_pred[i])**2 for i in range(len(prices)))
                confidence = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
            
            return {
                'trend': trend,
                'average_price': sum(p['price'] for p in price_data) / len(price_data),
                'price_range': {
                    'min': min(p['price'] for p in price_data),
                    'max': max(p['price'] for p in price_data)
                },
                'confidence': confidence,
                'data_points': len(price_data)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing historical prices for item {item_id}: {str(e)}")
            raise
            
    async def predict_seasonal_demand(self, category: str) -> Dict[str, Any]:
        """
        Predict seasonal demand patterns for a category.
        
        Args:
            category: The category to analyze
            
        Returns:
            Dictionary containing seasonal demand analysis
        """
        try:
            # Get all orders in this category from the past year
            one_year_ago = datetime.now() - timedelta(days=365)
            
            items = await self.db.item.find_many(
                where={
                    'detectedCategory': category,
                    'listings': {
                        'some': {
                            'orders': {
                                'some': {
                                    'createdAt': {
                                        'gte': one_year_ago
                                    }
                                }
                            }
                        }
                    }
                },
                include={
                    'listings': {
                        'include': {
                            'orders': True
                        }
                    }
                }
            )
            
            if not items:
                return {
                    'pattern': 'insufficient_data',
                    'peak_months': [],
                    'confidence': 0.0
                }
            
            # Aggregate orders by month
            monthly_orders = defaultdict(int)
            for item in items:
                for listing in item.listings:
                    for order in listing.orders:
                        if order.status == 'completed':
                            month = order.createdAt.month
                            monthly_orders[month] += 1
            
            if not monthly_orders:
                return {
                    'pattern': 'insufficient_data',
                    'peak_months': [],
                    'confidence': 0.0
                }
            
            # Find peak months (months with orders > average)
            avg_orders = sum(monthly_orders.values()) / len(monthly_orders)
            peak_months = [
                month for month, count in monthly_orders.items()
                if count > avg_orders
            ]
            
            # Determine seasonal pattern
            if len(monthly_orders) < 6:
                pattern = 'insufficient_data'
                confidence = 0.0
            else:
                # Check if peaks are clustered
                peak_months.sort()
                gaps = [peak_months[i+1] - peak_months[i] for i in range(len(peak_months)-1)]
                
                if len(peak_months) <= 2:
                    pattern = 'minimal_seasonality'
                elif max(gaps) > 4:
                    pattern = 'multi_season'
                else:
                    pattern = 'single_season'
                
                # Calculate confidence based on data consistency
                consistency = len(monthly_orders) / 12  # How many months we have data for
                peak_strength = max(monthly_orders.values()) / avg_orders
                confidence = min(consistency * 0.7 + (peak_strength - 1) * 0.3, 1.0)
            
            return {
                'pattern': pattern,
                'peak_months': peak_months,
                'monthly_distribution': dict(monthly_orders),
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Error predicting seasonal demand for category {category}: {str(e)}")
            raise
            
    async def analyze_competitive_pricing(self, item_id: str) -> Dict[str, Any]:
        """
        Analyze competitive pricing across marketplaces.
        
        Args:
            item_id: The ID of the item to analyze
            
        Returns:
            Dictionary containing competitive pricing analysis
        """
        try:
            # Get item and its current listings
            item = await self.db.item.find_unique(
                where={'id': item_id},
                include={
                    'listings': {
                        'include': {
                            'marketResearch': True
                        }
                    }
                }
            )
            
            if not item:
                return {
                    'recommendation': 'insufficient_data',
                    'price_points': {},
                    'confidence': 0.0
                }
            
            # Aggregate pricing data by marketplace
            marketplace_prices = defaultdict(list)
            for listing in item.listings:
                if listing.marketResearch:
                    for research in listing.marketResearch:
                        if research.competitorPrices:
                            prices = research.competitorPrices.get('prices', [])
                            marketplace_prices[listing.marketplace].extend(prices)
            
            if not marketplace_prices:
                return {
                    'recommendation': 'insufficient_data',
                    'price_points': {},
                    'confidence': 0.0
                }
            
            # Calculate price points for each marketplace
            price_points = {}
            overall_min = float('inf')
            overall_max = 0
            
            for marketplace, prices in marketplace_prices.items():
                if prices:
                    avg_price = sum(prices) / len(prices)
                    price_points[marketplace] = {
                        'average': avg_price,
                        'median': sorted(prices)[len(prices)//2],
                        'min': min(prices),
                        'max': max(prices),
                        'sample_size': len(prices)
                    }
                    overall_min = min(overall_min, min(prices))
                    overall_max = max(overall_max, max(prices))
            
            # Generate pricing recommendation
            if len(price_points) >= 2:
                # Complex recommendation based on market position
                lowest_avg = min(data['average'] for data in price_points.values())
                highest_avg = max(data['average'] for data in price_points.values())
                
                if highest_avg - lowest_avg < lowest_avg * 0.1:
                    recommendation = 'match_market'
                    target_price = lowest_avg
                else:
                    # Recommend slight undercutting of higher-priced marketplaces
                    target_price = highest_avg * 0.95
                    recommendation = 'competitive_advantage'
                
                confidence = min(
                    sum(data['sample_size'] for data in price_points.values()) / 20,
                    1.0
                )
            else:
                recommendation = 'single_marketplace'
                target_price = next(iter(price_points.values()))['average']
                confidence = 0.5
            
            return {
                'recommendation': recommendation,
                'target_price': target_price,
                'price_points': price_points,
                'market_spread': {
                    'min': overall_min,
                    'max': overall_max
                },
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Error analyzing competitive pricing for item {item_id}: {str(e)}")
            raise

async def update_analytics_data(listing_id: str, market_data: Dict[str, Any]) -> None:
    """
    Update analytics data for a listing based on market research data.
    
    Args:
        listing_id: The ID of the listing to update analytics for
        market_data: Market research data for the listing
    """
    try:
        # Calculate market analysis metrics based on monitoring config
        current_time = datetime.utcnow()
        data_timestamp = datetime.fromisoformat(market_data["timestamp"])
        data_age_hours = (current_time - data_timestamp).total_seconds() / 3600

        # Calculate price accuracy (deviation from market average)
        current_price = market_data["current_data"].get("price", 0)
        market_prices = [p for p in market_data["current_data"].get("competitor_prices", []) if p > 0]
        market_avg = sum(market_prices) / len(market_prices) if market_prices else current_price
        price_deviation = abs(current_price - market_avg) / market_avg if market_avg > 0 else 0

        # Calculate coverage rate (percentage of data points available)
        expected_data_points = ["price", "competitor_prices", "condition", "description"]
        available_points = sum(1 for point in expected_data_points if market_data["current_data"].get(point))
        coverage_rate = available_points / len(expected_data_points)

        analytics_service = AnalyticsService()
        await analytics_service.update_analytics_data(
            listing_id=listing_id,
            data={
                "market_data": market_data,
                "last_updated": current_time.isoformat(),
                "metrics": {
                    "price_accuracy": 1 - price_deviation,  # Convert deviation to accuracy
                    "data_freshness": 1 - min(data_age_hours / 24, 1),  # Normalize to 0-1 range
                    "coverage_rate": coverage_rate
                }
            }
        )
        logger.info(f"Updated analytics data for listing {listing_id} with market analysis metrics")
    except Exception as e:
        logger.error(f"Failed to update analytics data for listing {listing_id}: {str(e)}")
        raise

async def run_market_research(
    item_ids: List[str],
    days_history: Optional[int] = 30
) -> None:
    """
    Run the market research job and update analytics.
    
    Args:
        item_ids: List of item identifiers to research
        days_history: Number of days of price history to collect
    """
    job = MarketResearchJob()
    try:
        results = await job.collect_market_data(item_ids, days_history)
        
        # Update analytics data for each item
        for item_id, market_data in results.items():
            if "error" not in market_data:
                await update_analytics_data(item_id, market_data)
        
        logger.info(f"Market research and analytics update completed. Results: {results}")
        
    except Exception as e:
        logger.error(f"Failed to run market research: {str(e)}")
        raise
