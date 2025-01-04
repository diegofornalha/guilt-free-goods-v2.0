from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from ..db import get_db
from prisma import models

router = APIRouter()

class MessageCreate(BaseModel):
    conversation_id: int
    sender: str
    content: str

@router.post("/message")
async def create_message(payload: MessageCreate, db = Depends(get_db)):
    try:
        # Verify conversation exists
        conversation = await db.conversation.find_unique(
            where={"id": payload.conversation_id}
        )
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        # Create new message
        message = await db.message.create(
            data={
                "conversationId": payload.conversation_id,
                "sender": payload.sender,
                "content": payload.content
            }
        )
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
