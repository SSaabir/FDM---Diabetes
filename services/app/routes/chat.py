"""
Chat API Routes
Handles AI-powered diabetes chat assistance
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..utils.auth import get_current_user
from ..models.user import User
from ..services.chat import chat_service
from ..schemas.chat import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    SuggestedQuestionsResponse
)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the diabetes AI chat assistant
    """
    try:
        # Prepare context with user info if needed
        user_context = {
            "user_id": current_user.id,
            "user_email": current_user.email,
            "conversation_context": chat_request.context
        }
        
        # Generate AI response
        response = chat_service.generate_response(
            user_message=chat_request.message,
            user_id=str(current_user.id),
            context=user_context
        )
        
        return ChatResponse(
            message=response["message"],
            intent=response["intent"],
            suggestions=response.get("suggestions", []),
            source=response.get("source", "ai_assistant"),
            urgency=response.get("urgency", "normal"),
            timestamp=response.get("timestamp")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

@router.get("/chat/history", response_model=ConversationHistoryResponse)
async def get_chat_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """
    Get conversation history for the current user
    """
    try:
        history = chat_service.get_conversation_history(
            user_id=str(current_user.id),
            limit=limit
        )
        
        return ConversationHistoryResponse(
            messages=history,
            total_messages=len(history),
            user_id=str(current_user.id)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving chat history: {str(e)}"
        )

@router.delete("/chat/history")
async def clear_chat_history(
    current_user: User = Depends(get_current_user)
):
    """
    Clear conversation history for the current user
    """
    try:
        success = chat_service.clear_conversation(str(current_user.id))
        
        if success:
            return {"message": "Chat history cleared successfully"}
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to clear chat history"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing chat history: {str(e)}"
        )

@router.get("/chat/suggestions", response_model=SuggestedQuestionsResponse)
async def get_suggested_questions(
    current_user: User = Depends(get_current_user)
):
    """
    Get suggested questions based on conversation context
    """
    try:
        suggestions = chat_service.get_suggested_questions(str(current_user.id))
        
        return SuggestedQuestionsResponse(
            suggestions=suggestions,
            user_id=str(current_user.id)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving suggestions: {str(e)}"
        )

@router.post("/chat/quick-response")
async def quick_chat_response(
    message: str,
    current_user: User = Depends(get_current_user)
):
    """
    Get a quick response without storing in conversation history
    """
    try:
        # Use a temporary user ID for quick responses
        temp_user_id = f"temp_{current_user.id}"
        
        response = chat_service.generate_response(
            user_message=message,
            user_id=temp_user_id,
            context={"quick_response": True}
        )
        
        # Clear the temporary conversation
        chat_service.clear_conversation(temp_user_id)
        
        return {
            "message": response["message"],
            "intent": response["intent"],
            "suggestions": response.get("suggestions", [])
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating quick response: {str(e)}"
        )