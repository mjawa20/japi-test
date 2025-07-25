from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.database import get_db
from app.shared.deps import get_current_active_user
from . import schemas, services, repository
from app.modules.users.models import User

router = APIRouter(prefix="/chats", tags=["chats"])

def get_chat_repository(db: Session = Depends(get_db)):
    return repository.ChatRepository(db)

def get_chat_service(chat_repo: repository.ChatRepository = Depends(get_chat_repository)):
    return services.ChatService(chat_repo)

@router.post("/", response_model=schemas.ChatResponse)
async def send_message(
    message: schemas.MessageBase,
    current_user: User = Depends(get_current_active_user),
    chat_service: services.ChatService = Depends(get_chat_service)
):
    """
    Send a message to the AI tutor.
    For new users, this will handle the onboarding flow automatically.
    """
    try:
        return await chat_service.send_message(
            message_content=message.content,
            current_user=current_user
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/", response_model=List[schemas.MessageResponse])
async def get_chat_history(
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    chat_service: services.ChatService = Depends(get_chat_service)
):
    """Get chat history for the current user"""
    return chat_service.get_chat_history(current_user, limit=limit)

@router.delete("/", status_code=status.HTTP_200_OK)
async def clear_chat_history(
    current_user: User = Depends(get_current_active_user),
    chat_service: services.ChatService = Depends(get_chat_service)
):
    """Clear chat history for the current user"""
    chat_service.clear_chat_history(current_user)
    return {"message": "Chat history cleared successfully"}