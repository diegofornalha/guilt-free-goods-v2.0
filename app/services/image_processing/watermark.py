"""
Watermark Application Service

This module provides watermark application features:
- Text watermark application
- Watermark positioning
- Opacity control
- Multi-line support
"""

from typing import Tuple, Optional, Union
from PIL import Image, ImageDraw, ImageFont, ImageFont as PILImageFont
import io
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class WatermarkService:
    """Handles watermark application to images."""
    
    def __init__(self):
        """Initialize watermark service with default settings."""
        self.default_font_size = 36
        self.default_opacity = 128  # 0-255, where 255 is fully opaque
        self.default_color: Tuple[int, int, int] = (255, 255, 255)  # White
        self.default_position = 'bottom-right'
        self.padding = 20  # Padding from edges
        
        # Load default font (fallback to basic font if custom font not available)
        try:
            font_path = Path(__file__).parent / "fonts" / "OpenSans-Regular.ttf"
            self.default_font = ImageFont.truetype(str(font_path), self.default_font_size)
        except Exception as e:
            logger.warning(f"Could not load custom font: {str(e)}")
            self.default_font = str(e)  # Store error message to indicate default font should be used
    
    def apply_watermark(
        self,
        image_data: bytes,
        text: str,
        position: Optional[str] = None,
        opacity: Optional[int] = None,
        font_size: Optional[int] = None,
        color: Optional[Tuple[int, int, int]] = None
    ) -> Tuple[bytes, dict]:
        """
        Apply watermark to the input image.
        
        Args:
            image_data: Raw image bytes
            text: Watermark text to apply
            position: Position of watermark ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
            opacity: Opacity level (0-255)
            font_size: Font size in pixels
            color: RGB color tuple for watermark
            
        Returns:
            Tuple containing:
            - Watermarked image bytes
            - Dictionary with watermark metrics
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGBA if necessary
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Create transparent overlay
            overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Configure watermark
            opacity = opacity or self.default_opacity
            font_size = font_size or self.default_font_size
            position = position or self.default_position
            color = color or self.default_color
            
            # Update color with opacity
            color_to_use = color if color is not None else self.default_color
            watermark_color = (*color_to_use, opacity)
            
            # Calculate text size and position
            # Use default font if custom font failed to load
            if isinstance(self.default_font, str):
                font = ImageFont.load_default()
            else:
                font = ImageFont.truetype(str(self.default_font), font_size)
                
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = int(text_bbox[2] - text_bbox[0])
            text_height = int(text_bbox[3] - text_bbox[1])
            
            # Calculate position
            x, y = self._calculate_position(
                position,
                image.size,
                (text_width, text_height)
            )
            
            # Draw watermark on overlay
            draw.text(
                (x, y),
                text,
                font=font,
                fill=watermark_color
            )
            
            # Composite the watermark onto the image
            watermarked = Image.alpha_composite(image, overlay)
            
            # Convert back to bytes
            output_buffer = io.BytesIO()
            watermarked.save(output_buffer, format='PNG', quality=95)
            final_image = output_buffer.getvalue()
            
            # Calculate metrics
            metrics = {
                'position': position,
                'opacity': opacity,
                'font_size': font_size,
                'text_size': (text_width, text_height),
                'color': color_to_use
            }
            
            return final_image, metrics
            
        except Exception as e:
            logger.error(f"Error applying watermark: {str(e)}")
            raise
    
    def _calculate_position(
        self,
        position: str,
        image_size: Tuple[int, int],
        text_size: Tuple[int, int]
    ) -> Tuple[int, int]:
        """Calculate watermark position coordinates."""
        img_width, img_height = image_size
        text_width, text_height = text_size
        
        positions = {
            'top-left': (
                self.padding,
                self.padding
            ),
            'top-right': (
                img_width - text_width - self.padding,
                self.padding
            ),
            'bottom-left': (
                self.padding,
                img_height - text_height - self.padding
            ),
            'bottom-right': (
                img_width - text_width - self.padding,
                img_height - text_height - self.padding
            ),
            'center': (
                (img_width - text_width) // 2,
                (img_height - text_height) // 2
            )
        }
        
        return positions.get(position, positions['bottom-right'])
