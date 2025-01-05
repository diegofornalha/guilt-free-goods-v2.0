"""
Image processing service package.

Provides functionality for:
- Product detection using Google Cloud Vision
- Image quality optimization
- Background processing
- Watermarking
"""

from .product_detector import ProductDetector
from .quality_optimizer import ImageOptimizer
from .background_processor import BackgroundProcessor
from .watermark import WatermarkGenerator

__all__ = [
    'ProductDetector',
    'ImageOptimizer',
    'BackgroundProcessor',
    'WatermarkGenerator'
]
