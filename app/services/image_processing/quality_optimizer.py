"""
Image Quality Optimization Service

This module provides automated image quality optimization features including:
- Lighting adjustment
- Contrast enhancement
- Sharpness optimization
- Resolution standardization
"""

from typing import Optional, Tuple
from PIL import Image, ImageEnhance
import io
import logging

logger = logging.getLogger(__name__)

class ImageQualityOptimizer:
    """Handles automated image quality optimization."""
    
    def __init__(self):
        self.target_resolution = (1200, 1200)  # Standard resolution for product images
        self.quality_threshold = 0.8  # Minimum quality score (0-1)
        
    def optimize_image(self, image_data: bytes) -> Tuple[bytes, dict]:
        """
        Optimize the input image by adjusting lighting, contrast, and sharpness.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Tuple containing:
            - Optimized image bytes
            - Dictionary with quality metrics
        """
        try:
            # Load image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Standardize resolution
            image = self._standardize_resolution(image)
            
            # Optimize image quality
            image = self._enhance_lighting(image)
            image = self._enhance_contrast(image)
            image = self._enhance_sharpness(image)
            
            # Convert back to bytes
            output_buffer = io.BytesIO()
            image.save(output_buffer, format='JPEG', quality=95)
            optimized_image = output_buffer.getvalue()
            
            # Calculate quality metrics
            metrics = self._calculate_quality_metrics(image)
            
            return optimized_image, metrics
            
        except Exception as e:
            logger.error(f"Error optimizing image: {str(e)}")
            raise
    
    def _standardize_resolution(self, image: Image.Image) -> Image.Image:
        """Standardize image resolution while maintaining aspect ratio."""
        width, height = image.size
        aspect_ratio = width / height
        
        if aspect_ratio > 1:
            new_width = min(width, self.target_resolution[0])
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, self.target_resolution[1])
            new_width = int(new_height * aspect_ratio)
            
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def _enhance_lighting(self, image: Image.Image) -> Image.Image:
        """Optimize image brightness and lighting."""
        enhancer = ImageEnhance.Brightness(image)
        brightness = self._analyze_brightness(image)
        
        if brightness < 0.4:  # Too dark
            return enhancer.enhance(1.3)
        elif brightness > 0.7:  # Too bright
            return enhancer.enhance(0.8)
        return image
    
    def _enhance_contrast(self, image: Image.Image) -> Image.Image:
        """Optimize image contrast."""
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(1.2)  # Slight contrast boost
    
    def _enhance_sharpness(self, image: Image.Image) -> Image.Image:
        """Optimize image sharpness."""
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(1.3)  # Moderate sharpness enhancement
    
    def _analyze_brightness(self, image: Image.Image) -> float:
        """
        Analyze average image brightness.
        Returns value between 0 (black) and 1 (white).
        """
        grayscale = image.convert('L')
        histogram = grayscale.histogram()
        pixels = sum(histogram)
        brightness = sum(i * pixels for i, pixels in enumerate(histogram)) / (255 * pixels)
        return brightness
    
    def _calculate_quality_metrics(self, image: Image.Image) -> dict:
        """Calculate image quality metrics."""
        return {
            'resolution': image.size,
            'brightness': self._analyze_brightness(image),
            'aspect_ratio': image.size[0] / image.size[1],
            'format': image.format,
            'mode': image.mode
        }
