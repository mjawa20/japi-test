from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

from . import schemas, repository, models
from app.config.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

class UserService:
    def __init__(self, user_repo: repository.UserRepository):
        self.user_repo = user_repo

    def create_user(self, user: schemas.UserCreate) -> schemas.UserResponse:
        db_user = self.user_repo.get_user_by_email(user.email)
        if db_user:
            raise ValueError("Email already registered")
        
        hashed_password = get_password_hash(user.password)
        user_data = user.model_dump(exclude={"password"})
        return self.user_repo.create_user({
            **user_data,
            "hashed_password": hashed_password,
            "is_onboarded": False,
            "is_active": True
        })

    def login(self, email: str, password: str) -> schemas.Token:
        user = self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Incorrect email or password")
        
        if not user.is_active:
            raise ValueError("Inactive user")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return schemas.Token(access_token=access_token)

    def get_user_by_email(self, email: str) -> Optional[schemas.UserResponse]:
        user = self.user_repo.get_user_by_email(email)
        if not user:
            return None
        return schemas.UserResponse.model_validate(user.__dict__)

    def get_user(self, user_id: int) -> Optional[schemas.UserResponse]:
        user = self.user_repo.get_user(user_id)
        if not user:
            return None
        return schemas.UserResponse.model_validate(user.__dict__)

    def complete_onboarding(
        self, 
        user: models.User, 
        onboarding_data: schemas.OnboardingRequest
    ) -> models.User:
        """Complete user onboarding with English level and learning goal"""
        user.english_level = onboarding_data.english_level
        user.learning_goal = onboarding_data.learning_goal
        user.is_onboarded = True
        
        # Update the user with the new onboarding data
        return self.user_repo.update_user(user)