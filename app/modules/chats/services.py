from typing import List, Optional, Dict, Any
from datetime import datetime
import re

from . import schemas, repository
from app.infrastructure.ai_service import ai as ai_service, OnboardingStep
from app.modules.users.models import User

class ChatService:
    def __init__(self, chat_repo: repository.ChatRepository):
        self.chat_repo = chat_repo
        
    async def _extract_english_level(self, text: str) -> Optional[str]:
        """Extract English level from user's message"""
        text = text.lower()
        if 'beginner' in text:
            return 'beginner'
        elif 'intermediate' in text:
            return 'intermediate'
        elif 'advanced' in text:
            return 'advanced'
        return None

    async def _handle_onboarding_flow(
        self,
        current_user: User,
        user_message: str,
        previous_messages: List[Any]
    ) -> schemas.ChatResponse:
        """Handle the onboarding conversation flow for new users"""
        conversation_history = []
        
        for msg in previous_messages:
            try:
                role = str(msg.role) if hasattr(msg, 'role') else 'user'
                content = str(msg.content) if hasattr(msg, 'content') else str(msg)
                conversation_history.append({
                    'role': role.lower(),
                    'content': content
                })
            except Exception as e:
                print(f"Skipping invalid message: {e}")
                continue
        
        current_step = ai_service._detect_onboarding_step(conversation_history)
        
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        onboarding_response = ai_service.generate_onboarding_response(
            user_name=current_user.full_name or current_user.username,
            conversation_history=conversation_history,
            user_goal=current_user.learning_goal,
            user_level=current_user.english_level
        )
        
        new_step = ai_service._detect_onboarding_step(conversation_history + [
            {'role': 'ai', 'content': onboarding_response}
        ])
        
        if current_step == OnboardingStep.ASK_GOAL and new_step == OnboardingStep.ASK_LEVEL:
            current_user.learning_goal = user_message
        
        if current_step == OnboardingStep.ASK_LEVEL and 'beginner/intermediate/advanced' in onboarding_response.lower():
            pass
        elif current_step == OnboardingStep.ASK_LEVEL and not current_user.english_level:
            english_level = await self._extract_english_level(user_message)
            if english_level:
                current_user.english_level = english_level
        
        if current_user.learning_goal and current_user.english_level:
            current_user.is_onboarded = True
        
        ai_message = schemas.MessageCreate(
            content=onboarding_response,
            role='ai'
        )
        
        db_ai_message = self.chat_repo.create_message(
            ai_message,
            current_user.id
        )
        
        self.chat_repo.db.commit()
        
        updated_history = self.chat_repo.get_chat_history(current_user.id, limit=20)
        
        history_responses = [
            schemas.MessageResponse(
                id=msg.id,
                content=msg.content,
                role=msg.role,
                user_id=msg.user_id,
                created_at=msg.created_at
            )
            for msg in updated_history
        ]
        
        return schemas.ChatResponse(
            message=schemas.MessageResponse(
                id=db_ai_message.id,
                content=db_ai_message.content,
                role=db_ai_message.role,
                user_id=db_ai_message.user_id,
                created_at=db_ai_message.created_at
            ),
            history=history_responses,
            is_onboarded=current_user.is_onboarded
        )

    async def send_message(
        self, 
        message_content: str, 
        current_user: User
    ) -> schemas.ChatResponse:
        user_message = schemas.MessageCreate(
            content=message_content,
            role=schemas.MessageRole.USER
        )
        db_user_message = self.chat_repo.create_message(user_message, current_user.id)
        
        if not current_user.is_onboarded:
            db_messages = self.chat_repo.get_chat_history(current_user.id, limit=10)
            sorted_messages = sorted(db_messages, key=lambda x: getattr(x, 'created_at', datetime.min))
            return await self._handle_onboarding_flow(current_user, message_content, sorted_messages)
        
        try:
            messages = self.chat_repo.get_chat_history(current_user.id, limit=1)
            
            conversation_history = [
                {
                    "role": "ai" if msg.role == schemas.MessageRole.AI else "user",
                    "content": msg.content
                }
                for msg in messages
            ]
            
            ai_response = ai_service.generate_chat_response(
                conversation_history=conversation_history,
                user_name=current_user.full_name or current_user.username,
                user_level=current_user.english_level
            )
            
            ai_message = schemas.MessageCreate(
                content=ai_response,
                role=schemas.MessageRole.AI
            )
            db_ai_message = self.chat_repo.create_message(ai_message, current_user.id)
            
            return schemas.ChatResponse(
                message=schemas.MessageResponse(
                    id=db_ai_message.id,
                    content=db_ai_message.content,
                    role=db_ai_message.role,
                    user_id=db_ai_message.user_id,
                    created_at=db_ai_message.created_at
                ),
                is_onboarded=True
            )
            
        except Exception as e:
            raise Exception(f"Error processing chat message: {str(e)}")
    
    def get_chat_history(
        self, 
        current_user: User,
        limit: int = 20
    ) -> List[schemas.MessageResponse]:
        messages = self.chat_repo.get_chat_history(current_user.id, limit=limit)
        return [
            schemas.MessageResponse(
                id=msg.id,
                content=msg.content,
                role=msg.role,
                user_id=msg.user_id,
                created_at=msg.created_at
            )
            for msg in messages
        ]
    
    def clear_chat_history(self, current_user: User) -> None:
        self.chat_repo.delete_messages(current_user.id)