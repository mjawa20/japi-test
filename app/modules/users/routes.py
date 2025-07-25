from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.shared.deps import get_current_active_user
from . import schemas, services, repository, models

router = APIRouter(prefix="/users", tags=["users"])

def get_user_repository(db: Session = Depends(get_db)):
    return repository.UserRepository(db)

def get_user_service(user_repo: repository.UserRepository = Depends(get_user_repository)):
    return services.UserService(user_repo)

@router.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: schemas.UserCreate,
    user_service: services.UserService = Depends(get_user_service)
):
    """Create a new user account"""
    try:
        return user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=schemas.Token)
async def login(
    login_data: schemas.UserLogin,
    user_service: services.UserService = Depends(get_user_service)
):
    """Login with email and password, get an access token"""
    try:
        return user_service.login(
            email=login_data.email,
            password=login_data.password
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(
    current_user: models.User = Depends(get_current_active_user)
):
    """Get current user details"""
    return current_user