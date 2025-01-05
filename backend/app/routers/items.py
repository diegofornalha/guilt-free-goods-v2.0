from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db_for_route
from ..db_client import DatabaseClient

router = APIRouter()

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    condition: str
    brand: Optional[str] = None
    category: Optional[str] = None
    detection_score: Optional[float] = None
    image_quality_score: Optional[float] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

async def get_db_client(session: AsyncSession = Depends(get_db_for_route)) -> DatabaseClient:
    """Get database client from session."""
    return DatabaseClient(session)

@router.post("/", response_model=Item)
async def create_item(
    item: ItemCreate,
    db: DatabaseClient = Depends(get_db_client)
):
    """Create a new item."""
    try:
        created_item = await db.item.create({
            "data": {
                "title": item.title,
                "description": item.description,
                "price": item.price,
                "condition": item.condition,
                "brand": item.brand,
                "category": item.category,
                "detection_score": item.detection_score,
                "image_quality_score": item.image_quality_score
            }
        })
        return created_item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{item_id}", response_model=Item)
async def get_item(
    item_id: str,
    db: DatabaseClient = Depends(get_db_client)
):
    """Get an item by ID."""
    item = await db.item.find_unique(where={"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/", response_model=List[Item])
async def list_items(
    skip: int = 0,
    limit: int = 10,
    db: DatabaseClient = Depends(get_db_client)
):
    """List items with pagination."""
    items = await db.item.find_many(
        skip=skip,
        take=limit,
        order={"created_at": "desc"}
    )
    return items

@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: str,
    item: ItemCreate,
    db: DatabaseClient = Depends(get_db_client)
):
    """Update an item."""
    try:
        updated_item = await db.item.update(
            where={"id": item_id},
            data={
                "title": item.title,
                "description": item.description,
                "price": item.price,
                "condition": item.condition,
                "brand": item.brand,
                "category": item.category,
                "detection_score": item.detection_score,
                "image_quality_score": item.image_quality_score
            }
        )
        return updated_item
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/{item_id}")
async def delete_item(
    item_id: str,
    db: DatabaseClient = Depends(get_db_client)
):
    """Delete an item."""
    try:
        await db.item.delete(where={"id": item_id})
        return {"message": "Item deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Item not found")
