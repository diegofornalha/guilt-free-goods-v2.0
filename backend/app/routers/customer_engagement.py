from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from ..db import get_db, db
from ..services.nlp.nlp_service import response_generator

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
        # Generate automated response
        auto_response = response_generator.generate_response(payload.content)
        
        # Create automated response message
        auto_message = await db.message.create(
            data={
                "conversationId": payload.conversation_id,
                "sender": "system",
                "content": auto_response
            }
        )
        
        return {
            "user_message": message,
            "auto_response": auto_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
