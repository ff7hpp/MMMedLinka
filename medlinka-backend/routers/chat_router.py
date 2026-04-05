import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from auth import get_current_user
from services.wolfram_service import fetch_wolfram_data
from services.gemini_service import get_gemini_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["AI Chat"])

@router.post("/send")
async def send_chat_message(
    chat_input: schemas.ChatMessage,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_msg = chat_input.message
    
    # Save user message to DB
    user_history = models.ChatHistory(user_id=current_user.id, role="user", message=user_msg)
    db.add(user_history)
    db.commit()

    # Determine if we need Wolfram facts by looking for medical keywords
    query_lower = user_msg.lower()
    wolfram_context = ""
    source = "gemini"
    
    # Basic keyword check to decide if Wolfram should be used
    medical_keywords = ["side effect", "drug", "interaction", "dose", "mg", "symptom", "medicine"]
    if any(keyword in query_lower for keyword in medical_keywords):
        wolfram_context = await fetch_wolfram_data(user_msg)
        if wolfram_context:
            source = "wolfram+gemini"

    # Get Gemini response
    try:
        reply = await get_gemini_response(user_msg, context=wolfram_context)
    except Exception as e:
        logger.error(f"Gemini AI error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

    # Save bot message to DB
    bot_history = models.ChatHistory(user_id=current_user.id, role="bot", message=reply)
    db.add(bot_history)
    db.commit()

    # Retrieve recent history
    history = db.query(models.ChatHistory).filter(models.ChatHistory.user_id == current_user.id).order_by(models.ChatHistory.timestamp.asc()).all()

    return {
        "reply": reply,
        "source": source,
        "history": [{"role": h.role, "message": h.message, "timestamp": h.timestamp} for h in history]
    }
