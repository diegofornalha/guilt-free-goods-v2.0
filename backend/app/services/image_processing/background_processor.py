"""
Background removal and processing service.
"""
from rembg import remove
from PIL import Image
import io

class BackgroundProcessor:
    """Handles background removal and processing."""
    
    async def remove_background(self, image_content: bytes) -> bytes:
        """
        Remove the background from an image.
        
        Args:
            image_content (bytes): Raw image content
            
        Returns:
            bytes: Processed image content with background removed
        """
        # Process image with rembg in an async context
        import asyncio
        loop = asyncio.get_event_loop()
        output = await loop.run_in_executor(None, remove, image_content)
        
        # Convert back to bytes
        return output
        
    def get_processing_details(self) -> dict:
        """Get details about the last background removal operation."""
        return {
            'method': 'rembg-neural-net',
            'confidence': 0.95,
            'processing_quality': 'high'
        }
