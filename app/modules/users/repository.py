from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session

from . import models, schemas

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, user_id: int) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.id == user_id).first()
    
    def get_user_by_email(self, email: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.email == email).first()
    
    def get_user_by_username(self, username: str) -> Optional[models.User]:
        return self.db.query(models.User).filter(models.User.username == username).first()
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[models.User]:
        return self.db.query(models.User).offset(skip).limit(limit).all()
    
    def create_user(self, user_data: Dict[str, Any]) -> models.User:
        db_user = models.User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user_id: int, user_update: dict) -> Optional[models.User]:
        db_user = self.get_user(user_id)
        if not db_user:
            return None
            
        for field, value in user_update.items():
            setattr(db_user, field, value)
            
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete_user(self, user_id: int) -> bool:
        db_user = self.get_user(user_id)
        if not db_user:
            return False
            
        self.db.delete(db_user)
        self.db.commit()
        return True