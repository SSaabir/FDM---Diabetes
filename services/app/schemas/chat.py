"""
Chat Schemas
Pydantic models for chat API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    """Request model for chat messages"""
    
    message: str = Field(..., min_length=1, max_length=1000, description="User message to the AI assistant")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the conversation")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "How can I prevent diabetes?",
                "context": {"previous_topic": "risk_factors"}
            }
        }

class ChatResponse(BaseModel):
    """Response model for chat messages"""
    
    message: str = Field(..., description="AI assistant response")
    intent: str = Field(..., description="Detected intent of the user message")
    suggestions: List[str] = Field(..., description="Suggested follow-up questions")
    source: str = Field(..., description="Source of the response (e.g., prevention_guide)")
    urgency: str = Field("normal", description="Urgency level: normal, high")
    timestamp: Optional[str] = Field(None, description="Response timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Great question about diabetes prevention! Here are key strategies...",
                "intent": "prevention",
                "suggestions": ["Tell me about healthy foods", "Show me exercise plans"],
                "source": "prevention_guide",
                "urgency": "normal",
                "timestamp": "2024-01-01T12:00:00"
            }
        }

class ConversationMessage(BaseModel):
    """Individual message in conversation history"""
    
    type: str = Field(..., description="Message type: user or bot")
    message: str = Field(..., description="Message content")
    intent: Optional[str] = Field(None, description="Message intent (for bot messages)")
    timestamp: str = Field(..., description="Message timestamp")

class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history"""
    
    messages: List[ConversationMessage] = Field(..., description="List of conversation messages")
    total_messages: int = Field(..., description="Total number of messages")
    user_id: str = Field(..., description="User ID")
    
    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    {
                        "type": "user",
                        "message": "How can I prevent diabetes?",
                        "timestamp": "2024-01-01T12:00:00"
                    },
                    {
                        "type": "bot",
                        "message": "Great question about diabetes prevention!",
                        "intent": "prevention",
                        "timestamp": "2024-01-01T12:00:01"
                    }
                ],
                "total_messages": 2,
                "user_id": "12345"
            }
        }

class SuggestedQuestionsResponse(BaseModel):
    """Response model for suggested questions"""
    
    suggestions: List[str] = Field(..., description="List of suggested questions")
    user_id: str = Field(..., description="User ID")
    
    class Config:
        schema_extra = {
            "example": {
                "suggestions": [
                    "How can I prevent diabetes?",
                    "What foods should I eat?",
                    "What are the warning signs?"
                ],
                "user_id": "12345"
            }
        }

class QuickResponseRequest(BaseModel):
    """Request model for quick chat responses"""
    
    message: str = Field(..., min_length=1, max_length=500, description="Quick question for AI assistant")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "What is diabetes?"
            }
        }

class QuickResponseResponse(BaseModel):
    """Response model for quick chat responses"""
    
    message: str = Field(..., description="AI assistant response")
    intent: str = Field(..., description="Detected intent")
    suggestions: List[str] = Field(..., description="Related suggestions")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Diabetes is a condition where blood sugar levels are too high...",
                "intent": "general_info",
                "suggestions": ["Types of diabetes", "Risk factors", "Prevention tips"]
            }
        }