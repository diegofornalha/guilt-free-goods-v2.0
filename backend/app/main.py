from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import os
import logging

from .routers import marketplace, items, item_detection, inventory, customer_engagement, analytics, compliance
from .db import init_db, close_db, get_db

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="Guilt Free Goods API")

# Database lifecycle events
@app.on_event("startup")
async def startup_event():
    """Initialize database and background jobs."""
    await init_db()
    
    # Initialize background jobs
    from .services.background_jobs.item_recheck import ItemRecheckJob
    
    try:
        db = get_db()  # This returns a Prisma client instance
        recheck_job = ItemRecheckJob(db)
        await recheck_job.recheck_all_items()
    except Exception as e:
        logging.error(f"Failed to initialize background jobs: {str(e)}")
        # Don't raise the error to allow the app to start without background jobs

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

# Register global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global exception handler for HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler for unexpected errors."""
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configured for development - should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(marketplace.router)
app.include_router(items.router, prefix="/api/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Welcome to Guilt Free Goods API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include item detection router
app.include_router(item_detection.router)
app.include_router(inventory.router)

# Include customer engagement router
app.include_router(customer_engagement.router, prefix="/api/customer", tags=["customer"])

# Include analytics router
app.include_router(analytics.router)

# Include compliance router
app.include_router(compliance.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
