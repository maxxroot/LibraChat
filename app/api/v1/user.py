# app/api/v1/user.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import RegisterRequest, UserResponse, LoginRequest, UserLoginResponse
from app.services.auth_service import AuthService
from app.models import User
from app.database import get_async_session
from app.services.user_service import UserService
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register")
async def register_user(user_data: RegisterRequest, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    existing_user = await user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    new_user = await user_service.create_user(user_data)
    return {"message": "User registered successfully", "user_id": new_user.id}

@router.post("/login")
async def login_user(credentials: LoginRequest, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    user = await user_service.get_user_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token}


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    # Récupération de l'utilisateur par ID
    user = await UserService(session).get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Retourne les informations de l'utilisateur
    return user
