"""
Background Processing Service

This module provides automated background removal and standardization features:
- Smart background removal
- Background standardization
- Multi-angle photo compilation
"""

from typing import List, Tuple, Optional
from PIL import Image
import io
import logging
import requests
from rembg import remove
import numpy as np

logger = logging.getLogger(__name__)

class BackgroundProcessor:
    """Handles automated background removal and standardization."""
    
    def __init__(self):
        self.standard_bg_color = (255, 255, 255)  # White background
        self.output_size = (800, 800)  # Standard size for processed images
        
    def process_image(self, image_data: bytes) -> Tuple[bytes, dict]:
        """
        Remove background and standardize the image.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Tuple containing:
            - Processed image bytes
            - Dictionary with processing metrics
        """
        try:
            # Remove background
            processed_data = remove(image_data)
            
            # Load processed image
            image = Image.open(io.BytesIO(processed_data))
            
            # Standardize background
            standardized = self._standardize_background(image)
            
            # Convert back to bytes
            output_buffer = io.BytesIO()
            standardized.save(output_buffer, format='PNG', quality=95)
            final_image = output_buffer.getvalue()
            
            # Calculate metrics
            metrics = self._calculate_metrics(standardized)
            
            return final_image, metrics
            
        except Exception as e:
            logger.error(f"Error processing image background: {str(e)}")
            raise
    
    def compile_angles(self, image_list: List[bytes]) -> Tuple[bytes, dict]:
        """
        Compile multiple angles of the same product into a single image.
        
        Args:
            image_list: List of image bytes representing different angles
            
        Returns:
            Tuple containing:
            - Compiled image bytes
            - Dictionary with compilation metrics
        """
        try:
            processed_images = []
            
            # Process each image
            for img_data in image_list:
                processed_data, _ = self.process_image(img_data)
                img = Image.open(io.BytesIO(processed_data))
                processed_images.append(img)
            
            # Calculate grid dimensions
            grid_size = self._calculate_grid_size(len(processed_images))
            
            # Create compilation
            compilation = self._create_compilation(processed_images, grid_size)
            
            # Convert to bytes
            output_buffer = io.BytesIO()
            compilation.save(output_buffer, format='PNG', quality=95)
            final_compilation = output_buffer.getvalue()
            
            # Calculate metrics
            metrics = {
                'num_images': len(image_list),
                'grid_size': grid_size,
                'final_size': compilation.size
            }
            
            return final_compilation, metrics
            
        except Exception as e:
            logger.error(f"Error compiling image angles: {str(e)}")
            raise
    
    def _standardize_background(self, image: Image.Image) -> Image.Image:
        """Standardize image background to white."""
        # Convert to RGBA if necessary
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Create new white background
        background = Image.new('RGBA', image.size, self.standard_bg_color)
        
        # Composite the image onto the white background
        return Image.alpha_composite(background, image)
    
    def _calculate_grid_size(self, num_images: int) -> Tuple[int, int]:
        """Calculate optimal grid size for image compilation."""
        if num_images <= 1:
            return (1, 1)
        elif num_images <= 2:
            return (1, 2)
        elif num_images <= 4:
            return (2, 2)
        elif num_images <= 6:
            return (2, 3)
        else:
            return (3, 3)  # Maximum 9 images
    
    def _create_compilation(self, images: List[Image.Image], 
                          grid_size: Tuple[int, int]) -> Image.Image:
        """Create a grid compilation of multiple images."""
        rows, cols = grid_size
        cell_width = self.output_size[0] // cols
        cell_height = self.output_size[1] // rows
        
        # Create blank canvas
        compilation = Image.new('RGB', self.output_size, self.standard_bg_color)
        
        # Place images in grid
        for idx, img in enumerate(images):
            if idx >= rows * cols:
                break
                
            # Calculate position
            row = idx // cols
            col = idx % cols
            x = col * cell_width
            y = row * cell_height
            
            # Resize image to fit cell
            resized = img.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
            
            # Paste into compilation
            compilation.paste(resized, (x, y))
        
        return compilation
    
    def _calculate_metrics(self, image: Image.Image) -> dict:
        """Calculate processing metrics."""
        return {
            'size': image.size,
            'mode': image.mode,
            'format': image.format,
            'has_alpha': 'A' in image.mode
        }
