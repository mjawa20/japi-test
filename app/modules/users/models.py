from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.sql import func, expression
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base
from .schemas import UserRole, EnglishLevel

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    english_level = Column(SQLEnum(EnglishLevel), nullable=True)
    learning_goal = Column(Text, nullable=True)
    is_onboarded = Column(Boolean, server_default=expression.false(), default=False, nullable=False)
    is_active = Column(Boolean, server_default=expression.true(), default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.username}>"