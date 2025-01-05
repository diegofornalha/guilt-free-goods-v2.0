"""
Image watermarking service.
"""
from PIL import Image, ImageDraw, ImageFont
import io

class WatermarkGenerator:
    """Handles watermark generation and application."""
    
    def __init__(self):
        """Initialize watermark settings."""
        self.watermark_text = "Guilt Free Goods"
        self.font_size = 36
        self.opacity = 128  # Semi-transparent
    
    
    async def apply_watermark(self, image_content: bytes) -> bytes:
        """
        Apply watermark to the image.
        
        Args:
            image_content (bytes): Raw image content
            
        Returns:
            bytes: Image content with watermark
        """
        # Open image
        image = Image.open(io.BytesIO(image_content))
        
        # Create watermark layer
        watermark = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)
        
        # Calculate text position (bottom right corner)
        text_width = self.font_size * len(self.watermark_text) // 2
        text_height = self.font_size
        position = (
            image.size[0] - text_width - 20,
            image.size[1] - text_height - 20
        )
        
        # Draw watermark text
        draw.text(
            position,
            self.watermark_text,
            fill=(255, 255, 255, self.opacity),
            font=ImageFont.load_default()
        )
        
        # Combine images
        watermarked = Image.alpha_composite(image.convert('RGBA'), watermark)
        
        # Convert to bytes
        output = io.BytesIO()
        watermarked.save(output, format='PNG')
        return output.getvalue()
