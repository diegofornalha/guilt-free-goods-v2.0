from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import os

app = FastAPI(title="Guilt Free Goods API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configured for development - should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Guilt Free Goods API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Image Processing Routes
@app.post("/api/images/optimize")
async def optimize_image():
    """
    Endpoint for image quality optimization
    To be implemented with quality_optimizer.py
    """
    return JSONResponse(
        status_code=501,
        content={"message": "Endpoint under development"}
    )

@app.post("/api/images/remove-background")
async def remove_background():
    """
    Endpoint for background removal
    To be implemented with background_processor.py
    """
    return JSONResponse(
        status_code=501,
        content={"message": "Endpoint under development"}
    )

@app.post("/api/images/detect-product")
async def detect_product():
    """
    Endpoint for product detection
    To be implemented with product_detector.py
    """
    return JSONResponse(
        status_code=501,
        content={"message": "Endpoint under development"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
