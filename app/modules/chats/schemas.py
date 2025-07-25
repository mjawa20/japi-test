from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class  MessageRole(str, Enum):
    USER = "user"
    AI = "ai"
    SYSTEM = "system"

class MessageBase(BaseModel):
    content: str = Field(..., description="The content of the message")

class MessageCreate(BaseModel):
    content: str = Field(..., description="The content of the message")
    role: MessageRole = Field(..., description="The role of the message sender")

class MessageUpdate(BaseModel):
    content: Optional[str] = Field(None, description="The updated content of the message")
    role: Optional[MessageRole] = Field(None, description="The updated role of the message sender")

class MessageResponse(MessageBase):
    id: int
    role: MessageRole = Field(..., description="The role of the message sender (user or ai)")
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str = Field(..., description="The message content from the user")

class ChatResponse(BaseModel):
    message: MessageResponse = Field(..., description="The AI's response message")
    is_onboarding_complete: bool = Field(False, description="Whether the user has completed onboarding")