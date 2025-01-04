"""
Product Detection Service

This module provides AI-powered product recognition features:
- Item identification and categorization
- Brand and model detection
- Condition assessment
- Size detection
- Authenticity verification
"""

from typing import Dict, List, Optional, Tuple
import spacy
from google.cloud import vision
import io
import logging
import json
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

class ProductDetector:
    """Handles AI-powered product detection and analysis."""
    
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        self.confidence_threshold = 0.7
        self.condition_grades = ['New', 'Like New', 'Very Good', 'Good', 'Fair', 'Poor']
        
    def analyze_product(self, image_data: bytes) -> Dict:
        """
        Analyze product image using Google Cloud Vision API.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Prepare image for API
            image = vision.Image(content=image_data)
            
            # Run multiple detection features in parallel
            features = [
                vision.Feature(type_=vision.Feature.Type.OBJECT_LOCALIZATION),
                vision.Feature(type_=vision.Feature.Type.LOGO_DETECTION),
                vision.Feature(type_=vision.Feature.Type.LABEL_DETECTION),
                vision.Feature(type_=vision.Feature.Type.TEXT_DETECTION),
                vision.Feature(type_=vision.Feature.Type.IMAGE_PROPERTIES)
            ]
            
            # Perform batch annotation
            response = self.client.batch_annotate_images([
                vision.AnnotateImageRequest(image=image, features=features)
            ])
            
            # Process results
            result = response.responses[0]
            
            # Compile analysis results
            analysis = {
                'product': self._process_product_detection(result),
                'brand': self._process_brand_detection(result),
                'condition': self._assess_condition(result),
                'size': self._detect_size(result),
                'authenticity': self._verify_authenticity(result)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing product: {str(e)}")
            raise
    
    def _process_product_detection(self, result) -> Dict:
        """Process object localization and label detection results."""
        objects = []
        categories = []
        
        # Process detected objects
        for obj in result.localized_object_annotations:
            if obj.score >= self.confidence_threshold:
                objects.append({
                    'name': obj.name,
                    'confidence': obj.score,
                    'bounds': [(vertex.x, vertex.y) for vertex in obj.bounding_poly.normalized_vertices]
                })
        
        # Process detected labels
        for label in result.label_annotations:
            if label.score >= self.confidence_threshold:
                categories.append({
                    'name': label.description,
                    'confidence': label.score
                })
        
        return {
            'detected_objects': objects,
            'categories': categories
        }
    
    def _process_brand_detection(self, result) -> Dict:
        """Process logo detection and text detection for brand information."""
        brands = []
        
        # Process detected logos
        for logo in result.logo_annotations:
            if logo.score >= self.confidence_threshold:
                brands.append({
                    'name': logo.description,
                    'confidence': logo.score
                })
        
        # Process text for potential brand names
        if result.text_annotations:
            # First element contains all text
            text = result.text_annotations[0].description if result.text_annotations else ""
            
            # Extract brand names using spaCy NLP
            if text:
                nlp = spacy.load('en_core_web_sm')
                doc = nlp(text)
                
                # Extract proper nouns (potential brand names)
                potential_brands = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT']]
                potential_brands.extend([token.text for token in doc if token.pos_ == 'PROPN'])
                
                # Add extracted brands with lower confidence
                for brand in set(potential_brands):
                    brands.append({
                        'name': brand,
                        'confidence': 0.6,  # Lower confidence for NLP-extracted brands
                        'source': 'text'
                    })
            
        return {
            'detected_brands': brands,
            'extracted_text': text if 'text' in locals() else "",
            'potential_brands': list(set(potential_brands)) if 'potential_brands' in locals() else []
        }
    
    def _assess_condition(self, result) -> Dict:
        """
        Assess product condition based on visual features.
        Uses image properties and detected defects.
        """
        # Analyze image properties for condition assessment
        properties = result.image_properties_annotation
        
        # Calculate overall quality score based on image properties
        quality_score = self._calculate_quality_score(properties)
        
        # Determine condition grade based on quality score
        condition_grade = self._determine_condition_grade(quality_score)
        
        return {
            'grade': condition_grade,
            'quality_score': quality_score,
            'details': self._generate_condition_details(properties)
        }
    
    def _detect_size(self, result) -> Dict:
        """
        Detect product size using object detection and reference objects.
        """
        # Get detected objects with their bounding boxes
        objects = result.localized_object_annotations
        
        # Find reference objects for size estimation
        reference_objects = self._find_reference_objects(objects)
        
        # Calculate approximate dimensions
        dimensions = self._calculate_dimensions(objects, reference_objects)
        
        
        return {
            'estimated_dimensions': dimensions,
            'reference_objects': reference_objects,
            'confidence': self._calculate_size_confidence(reference_objects)
        }
    
    def _verify_authenticity(self, result) -> Dict:
        """
        Verify product authenticity based on brand detection and visual features.
        """
        # Analyze brand detection results
        brand_results = self._process_brand_detection(result)
        
        # Calculate authenticity score
        auth_score = self._calculate_authenticity_score(
            brand_results,
            result.image_properties_annotation
        )
        
        return {
            'authenticity_score': auth_score,
            'verification_details': self._generate_verification_details(brand_results),
            'confidence': min(1.0, auth_score / 0.8)  # Normalize confidence
        }
    
    def _calculate_quality_score(self, properties) -> float:
        """Calculate overall quality score from image properties."""
        # Analyze color distribution
        colors = properties.dominant_colors.colors
        
        # Calculate color variance as quality indicator
        color_scores = [color.score * color.pixel_fraction for color in colors]
        return min(1.0, sum(color_scores) * 1.5)  # Normalize to 0-1
    
    def _determine_condition_grade(self, quality_score: float) -> str:
        """Map quality score to condition grade."""
        if quality_score >= 0.9:
            return self.condition_grades[0]  # New
        elif quality_score >= 0.8:
            return self.condition_grades[1]  # Like New
        elif quality_score >= 0.7:
            return self.condition_grades[2]  # Very Good
        elif quality_score >= 0.6:
            return self.condition_grades[3]  # Good
        elif quality_score >= 0.4:
            return self.condition_grades[4]  # Fair
        else:
            return self.condition_grades[5]  # Poor
    
    def _generate_condition_details(self, properties) -> List[str]:
        """Generate detailed condition assessment."""
        details = []
        
        # Analyze color properties
        colors = properties.dominant_colors.colors
        if len(colors) > 0:
            main_color = colors[0]
            if main_color.score < 0.5:
                details.append("Color fading detected")
            
        # Analyze image quality metrics
        if main_color.score < 0.3:
            details.append("Significant color degradation")
        
        # Check color consistency
        color_variance = sum(abs(c.score - main_color.score) for c in colors[1:])
        if color_variance > 1.0:
            details.append("Uneven coloring or discoloration")
            
        # Check for potential damage indicators
        if len(colors) > 5 and max(c.pixel_fraction for c in colors) < 0.3:
            details.append("Possible surface irregularities detected")
            
        # Add wear level assessment
        wear_level = self._assess_wear_level(properties)
        if wear_level:
            details.append(f"Wear level: {wear_level}")
            
        return details
        
    def _assess_wear_level(self, properties) -> Optional[str]:
        """Assess wear level based on image properties."""
        colors = properties.dominant_colors.colors
        
        # Calculate wear indicators
        color_uniformity = max(c.pixel_fraction for c in colors)
        color_contrast = max(c.score for c in colors) - min(c.score for c in colors)
        
        if color_uniformity > 0.8 and color_contrast < 0.2:
            return "Minimal wear"
        elif color_uniformity > 0.6:
            return "Light wear"
        elif color_uniformity > 0.4:
            return "Moderate wear"
        else:
            return "Heavy wear"
    
    def _find_reference_objects(self, objects) -> List[Dict]:
        """Find objects that can be used as size reference."""
        reference_objects = []
        
        # Known size references (in cm)
        known_sizes = {
            'credit card': (8.5, 5.4),
            'smartphone': (15, 7),
            'coin': (2.5, 2.5),  # Average coin size
            'ruler': (30, 3)
        }
        
        for obj in objects:
            if obj.name.lower() in known_sizes:
                reference_objects.append({
                    'name': obj.name,
                    'known_size': known_sizes[obj.name.lower()],
                    'bounds': [(vertex.x, vertex.y) for vertex in obj.bounding_poly.normalized_vertices]
                })
        
        return reference_objects
    
    def _calculate_dimensions(self, objects, reference_objects) -> Optional[Dict]:
        """Calculate approximate dimensions using reference objects."""
        if not reference_objects:
            return None
            
        # Use the first reference object for calculation
        ref = reference_objects[0]
        ref_bounds = ref['bounds']
        ref_size = ref['known_size']
        
        # Calculate pixel to cm ratio
        pixel_to_cm = ref_size[0] / abs(ref_bounds[1][0] - ref_bounds[0][0])
        
        # Find main product object (usually the largest)
        product_obj = max(objects, key=lambda x: 
            abs((x.bounding_poly.normalized_vertices[1].x - 
                 x.bounding_poly.normalized_vertices[0].x) *
                (x.bounding_poly.normalized_vertices[2].y - 
                 x.bounding_poly.normalized_vertices[0].y)))
        
        # Calculate product dimensions
        width = abs(product_obj.bounding_poly.normalized_vertices[1].x - 
                   product_obj.bounding_poly.normalized_vertices[0].x) * pixel_to_cm
        height = abs(product_obj.bounding_poly.normalized_vertices[2].y - 
                    product_obj.bounding_poly.normalized_vertices[0].y) * pixel_to_cm
        
        return {
            'width': round(width, 1),
            'height': round(height, 1),
            'unit': 'cm'
        }
    
    def _calculate_size_confidence(self, reference_objects: List[Dict]) -> float:
        """Calculate confidence in size estimation."""
        if not reference_objects:
            return 0.0
        
        # More reference objects increase confidence
        base_confidence = min(1.0, len(reference_objects) * 0.4)
        
        # Average confidence based on reference object reliability
        reliability_scores = {
            'ruler': 0.9,
            'credit card': 0.8,
            'smartphone': 0.7,
            'coin': 0.6
        }
        
        reliability = sum(reliability_scores.get(ref['name'].lower(), 0.5) 
                        for ref in reference_objects) / len(reference_objects)
        
        return min(1.0, (base_confidence + reliability) / 2)
    
    def _calculate_authenticity_score(self, brand_results: Dict, 
                                    properties) -> float:
        """Calculate authenticity score based on brand detection and image quality."""
        # Calculate brand detection confidence
        brand_scores = [b.get('confidence', 0) for b in brand_results['detected_brands']]
        brand_confidence = max(brand_scores, default=0.4)  # Default if no brands detected
        
        # Analyze image quality as authenticity indicator
        quality_score = self._calculate_quality_score(properties)
        
        # Check for consistent brand appearance
        brand_consistency = self._check_brand_consistency(brand_results)
        
        # Calculate final authenticity score with weighted components
        weights = {
            'brand_confidence': 0.5,
            'quality': 0.3,
            'consistency': 0.2
        }
        
        auth_score = (
            weights['brand_confidence'] * brand_confidence +
            weights['quality'] * quality_score +
            weights['consistency'] * brand_consistency
        )
        
        return min(1.0, auth_score)
    
    def _generate_verification_details(self, brand_results: Dict) -> List[str]:
        """Generate detailed authenticity verification report."""
        details = []
        
        # Add brand detection details with confidence levels
        if brand_results['detected_brands']:
            for brand in brand_results['detected_brands']:
                confidence_level = "high" if brand['confidence'] > 0.8 else \
                                 "medium" if brand['confidence'] > 0.6 else "low"
                source = brand.get('source', 'visual')
                details.append(
                    f"Detected {brand['name']} brand with {confidence_level} confidence "
                    f"({source} detection, {brand['confidence']*100:.1f}%)"
                )
        else:
            details.append("Warning: No verified brands detected")
            
        # Add potential brand matches from text
        if brand_results.get('potential_brands'):
            details.append("Additional brand references found in text:")
            for brand in brand_results['potential_brands']:
                details.append(f"- Potential brand reference: {brand}")
        
        # Add verification status
        if not brand_results['detected_brands']:
            details.append("Authenticity verification: Insufficient brand information")
        elif max(b['confidence'] for b in brand_results['detected_brands']) < 0.6:
            details.append("Authenticity verification: Low confidence - manual review recommended")
        else:
            details.append("Authenticity verification: Passed automated checks")
        
        return details
        
    def _check_brand_consistency(self, brand_results: Dict) -> float:
        """Check consistency of brand detection across methods."""
        visual_brands = {b['name'].lower() for b in brand_results['detected_brands'] 
                        if b.get('source', 'visual') == 'visual'}
        text_brands = {b['name'].lower() for b in brand_results['detected_brands'] 
                      if b.get('source', 'text') == 'text'}
        
        # Calculate consistency score
        if not visual_brands and not text_brands:
            return 0.0
        elif not visual_brands or not text_brands:
            return 0.5
        
        # Check for brand name matches across methods
        matches = visual_brands.intersection(text_brands)
        consistency = len(matches) / max(len(visual_brands), len(text_brands))
        
        
        return consistency
