"""
Background job to re-check existing items using the product detector
"""
from typing import List
import asyncio
import logging
from prisma.client import Prisma
from ...services.image_processing.product_detector import ProductDetector
import aiohttp
import io

logger = logging.getLogger(__name__)

class ItemRecheckJob:
    """Background job to re-analyze existing items."""
    
    def __init__(self, db: Prisma):
        self.db = db
        self.detector = ProductDetector()
        
    async def recheck_all_items(self, batch_size: int = 10):
        """Re-analyze all items in batches."""
        try:
            # Get all items with images
            items = await self.db.item.find_many(
                where={
                    'imageUrls': {'not': []}  # Items with non-empty imageUrls
                }
            )
            
            # Process in batches
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                await self.process_batch(batch)
                logger.info(f"Processed batch {i//batch_size + 1}")
                
        except Exception as e:
            logger.error(f"Error in recheck_all_items: {str(e)}")
            raise
            
    async def process_batch(self, items: List):
        """Process a batch of items concurrently."""
        tasks = [self.recheck_item(item) for item in items]
        await asyncio.gather(*tasks)
        
    async def recheck_item(self, item):
        """Re-analyze a single item."""
        try:
            # Download first image for analysis
            if not item.imageUrls:
                return
                
            image_url = item.imageUrls[0]
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as response:
                    if response.status != 200:
                        logger.error(f"Failed to download image for item {item.id}")
                        return
                    image_data = await response.read()
            
            # Analyze image
            analysis = self.detector.analyze_product(image_data)
            
            # Update item with new analysis
            await self.db.item.update(
                where={'id': item.id},
                data={
                    'detectionScore': analysis['product'].get('confidence'),
                    'categoryConfidence': max(
                        (cat['confidence'] for cat in analysis['product']['categories']),
                        default=0.0
                    ),
                    'detectedCategory': analysis['product']['categories'][0]['name']
                    if analysis['product']['categories'] else None,
                    'detectedBrand': analysis['brand']['detected_brands'][0]['name']
                    if analysis['brand']['detected_brands'] else None,
                    'qualityScore': analysis['condition']['quality_score'],
                    'condition': analysis['condition']['grade'],
                    'dimensions': analysis['size'],
                    'defects': {
                        'details': analysis['condition']['details'],
                        'wear_level': analysis['condition'].get('wear_level')
                    }
                }
            )
            
            logger.info(f"Successfully re-analyzed item {item.id}")
            
        except Exception as e:
            logger.error(f"Error processing item {item.id}: {str(e)}")
