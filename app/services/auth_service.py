# app/services/auth_service.py

from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.core.security import verify_password
from app.models.user import User
from app.core.config import settings

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Vérification de l'email et du mot de passe lors de l'authentification
    async def authenticate_user(self, email: str, password: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalars().first()

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    # Création d'un access token avec le full_username dans le JWT
    async def create_access_token(self, user: User) -> str:
        to_encode = {
            "sub": user.full_username,  # Utilisation du full_username pour l'identification fédérée
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        print(f"Generating token for: {user.full_username}")  # Ajout de log pour vérification
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    # Gestion de la connexion de l'utilisateur
    async def login_user(self, email: str, password: str) -> str:
        user = await self.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Génération et retour du token JWT avec full_username
        return await self.create_access_token(user)
