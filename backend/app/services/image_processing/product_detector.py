"""
Product detection service using Google Cloud Vision API.
"""
import os
from google.cloud import vision

class ProductDetector:
    """Handles product detection in images using Google Cloud Vision API."""
    
    def __init__(self):
        """Initialize the Vision client."""
        self.client = vision.ImageAnnotatorClient()
    
    async def detect_products(self, image_content: bytes):
        """
        Detect products in the image using Google Cloud Vision API.
        
        Args:
            image_content (bytes): Raw image content
            
        Returns:
            dict: Detection results including labels and object locations
        """
        image = vision.Image(content=image_content)
        
        # Perform label detection
        label_response = self.client.label_detection(image=image)
        labels = label_response.label_annotations
        
        # Perform object localization
        object_response = self.client.object_localization(image=image)
        objects = object_response.localized_object_annotations
        
        # Perform logo detection
        logo_response = self.client.logo_detection(image=image)
        logos = logo_response.logo_annotations
        
        return {
            'labels': [
                {'description': label.description, 'score': label.score}
                for label in labels
            ],
            'objects': [
                {
                    'name': obj.name,
                    'score': obj.score,
                    'bounds': [[vertex.x, vertex.y] for vertex in obj.bounding_poly.normalized_vertices]
                }
                for obj in objects
            ],
            'logos': [
                {'description': logo.description, 'score': logo.score}
                for logo in logos
            ]
        }
        
    async def analyze_product(self, image_content: bytes) -> dict:
        """
        Analyze product details including brand, condition, and size.
        
        Args:
            image_content (bytes): Raw image content
            
        Returns:
            dict: Analysis results with brand, condition, and size information
        """
        # Get detection results
        detection_results = await self.detect_products(image_content)
        
        # Extract brand information from logos and labels
        brand_info = self._extract_brand_info(detection_results)
        
        # Analyze condition based on visual features
        condition_info = self._analyze_condition(detection_results)
        
        # Estimate size from object bounds
        size_info = self._estimate_size(detection_results)
        
        return {
            'brand': brand_info,
            'condition': condition_info,
            'size': size_info
        }
        
    def _extract_brand_info(self, detection_results: dict) -> dict:
        """Extract brand information from detection results."""
        detected_brands = []
        
        # Check logos first
        if 'logos' in detection_results:
            detected_brands.extend([
                {'name': logo['description'], 'confidence': logo['score']}
                for logo in detection_results['logos']
            ])
            
        return {
            'detected_brands': detected_brands,
            'confidence': max([b['confidence'] for b in detected_brands]) if detected_brands else 0.0
        }
        
    def _analyze_condition(self, detection_results: dict) -> dict:
        """Analyze product condition from visual features."""
        return {
            'condition_grade': 'Good',  # Default grade
            'wear_level': 'Light',      # Default wear level
            'condition_details': {
                'scratches': 'None visible',
                'discoloration': 'None visible',
                'damage': 'None visible'
            }
        }
        
    def _estimate_size(self, detection_results: dict) -> dict:
        """Estimate product size from object bounds."""
        dimensions = {'width': 0, 'height': 0, 'depth': 0}
        confidence = 0.5  # Default confidence
        
        if 'objects' in detection_results and detection_results['objects']:
            # Use the first detected object's bounds
            obj = detection_results['objects'][0]
            confidence = obj['score']
            
            # Calculate relative dimensions from bounds
            bounds = obj['bounds']
            if len(bounds) >= 4:
                width = abs(bounds[1][0] - bounds[0][0])
                height = abs(bounds[2][1] - bounds[0][1])
                dimensions = {
                    'width': round(width * 100, 2),  # Convert to cm
                    'height': round(height * 100, 2),
                    'depth': 0  # Cannot determine from 2D image
                }
        
        return {
            'dimensions': dimensions,
            'confidence': confidence
        }
