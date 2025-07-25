from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas

class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, message: schemas.MessageCreate, user_id: int) -> models.Message:
        """Create a new message"""
        db_message = models.Message(
            content=message.content,
            role=message.role,
            user_id=user_id
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return db_message

    def get_user_messages(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[models.Message]:
        """Get all messages for a specific user"""
        return (
            self.db.query(models.Message)
            .filter(models.Message.user_id == user_id)
            .order_by(models.Message.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def delete_messages(self, user_id: int) -> bool:
        """Delete all messages by user_id"""
        deleted_count = self.db.query(models.Message).filter(models.Message.user_id == user_id).delete()
        self.db.commit()
        return deleted_count > 0
    
    def get_chat_history(self, user_id: int, limit: int = 20) -> List[models.Message]:
        """Get the chat history for a user, most recent first"""
        return (
            self.db.query(models.Message)
            .filter(models.Message.user_id == user_id)
            .order_by(models.Message.created_at.desc())
            .limit(limit)
            .all()
        )