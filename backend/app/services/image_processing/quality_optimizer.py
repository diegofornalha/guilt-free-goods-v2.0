"""
Image quality optimization service.
"""
from PIL import Image
import io

class ImageOptimizer:
    """Handles image quality optimization."""
    
    def __init__(self):
        """Initialize the optimizer with default settings."""
        self.max_size = (1920, 1920)  # Max dimensions
        self.quality = 85  # JPEG quality
        self.format = 'JPEG'  # Output format
    
    async def optimize(self, image_content: bytes) -> bytes:
        """
        Optimize the image quality and size.
        
        Args:
            image_content (bytes): Raw image content
            
        Returns:
            bytes: Optimized image content
        """
        import asyncio
        
        def _optimize_image(image_content: bytes) -> bytes:
            # Open image from bytes
            image = Image.open(io.BytesIO(image_content))
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            
            # Resize if larger than max dimensions
            if image.size[0] > self.max_size[0] or image.size[1] > self.max_size[1]:
                image.thumbnail(self.max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image to bytes
            output = io.BytesIO()
            image.save(output, format=self.format, quality=self.quality, optimize=True)
            return output.getvalue()
        
        # Run CPU-intensive image processing in a thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _optimize_image, image_content)
        
    def get_optimization_details(self) -> dict:
        """Get details about the last optimization operation."""
        return {
            'format': self.format,
            'quality': self.quality,
            'max_dimensions': self.max_size,
            'optimization_level': 'high'
        }
