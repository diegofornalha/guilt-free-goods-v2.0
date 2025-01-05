"""
Item Detection Router

This module provides FastAPI endpoints for AI-powered item detection features:
- Image analysis
- Brand detection
- Condition assessment
- Size detection
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, List
import io
from ..services.image_processing.product_detector import ProductDetector
from ..services.image_processing.quality_optimizer import ImageOptimizer
from ..services.image_processing.background_processor import BackgroundProcessor

router = APIRouter(
    prefix="/api/item-detection",
    tags=["item-detection"]
)

# Initialize services
detector = ProductDetector()
optimizer = ImageOptimizer()
bg_processor = BackgroundProcessor()

@router.post("/analyze")
async def analyze_item(image: UploadFile = File(...)) -> Dict:
    """
    Analyze an item image using AI detection features.
    
    Args:
        image: Uploaded image file
        
    Returns:
        Dictionary containing analysis results
    """
    try:
        # Read image data
        contents = await image.read()
        
        # Analyze image using ProductDetector
        results = await detector.analyze_product(contents)
        
        return {
            "status": "success",
            "data": results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image: {str(e)}"
        )

@router.post("/optimize")
async def optimize_image(image: UploadFile = File(...)) -> Dict:
    """
    Optimize image quality using AI-powered enhancement.
    
    Args:
        image: Uploaded image file
        
    Returns:
        Dictionary containing optimized image data
    """
    try:
        contents = await image.read()
        optimized_image = await optimizer.optimize(contents)
        
        # Convert optimized image to base64 for JSON response
        import base64
        encoded_image = base64.b64encode(optimized_image).decode('utf-8')
        
        return {
            "status": "success",
            "data": {
                "optimized_image": encoded_image,
                "optimization_details": optimizer.get_optimization_details()
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error optimizing image: {str(e)}"
        )

@router.post("/remove-background")
async def remove_background(image: UploadFile = File(...)) -> Dict:
    """
    Remove image background using AI segmentation.
    
    Args:
        image: Uploaded image file
        
    Returns:
        Dictionary containing processed image data
    """
    try:
        contents = await image.read()
        processed_image = await bg_processor.remove_background(contents)
        
        # Convert processed image to base64 for JSON response
        import base64
        encoded_image = base64.b64encode(processed_image).decode('utf-8')
        
        return {
            "status": "success",
            "data": {
                "processed_image": encoded_image,
                "processing_details": bg_processor.get_processing_details()
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error removing background: {str(e)}"
        )

@router.post("/detect-brand")
async def detect_brand(image: UploadFile = File(...)) -> Dict:
    """
    Detect brand information from an item image.
    
    Args:
        image: Uploaded image file
        
    Returns:
        Dictionary containing brand detection results
    """
    try:
        contents = await image.read()
        results = await detector.analyze_product(contents)
        
        return {
            "status": "success",
            "data": results["brand"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting brand: {str(e)}"
        )

@router.post("/assess-condition")
async def assess_condition(image: UploadFile = File(...)) -> Dict:
    """
    Assess item condition from an image.
    
    Args:
        image: Uploaded image file
        
    Returns:
        Dictionary containing condition assessment results
    """
    try:
        contents = await image.read()
        results = await detector.analyze_product(contents)
        
        return {
            "status": "success",
            "data": results["condition"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error assessing condition: {str(e)}"
        )

@router.post("/detect-size")
async def detect_size(image: UploadFile = File(...)) -> Dict:
    """
    Detect item size from an image.
    
    Args:
        image: Uploaded image file
        
    Returns:
        Dictionary containing size detection results
    """
    try:
        contents = await image.read()
        results = await detector.analyze_product(contents)
        
        return {
            "status": "success",
            "data": results["size"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting size: {str(e)}"
        )
