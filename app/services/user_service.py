# app/services/user_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import RegisterRequest, UserResponse
from app.core.security import get_password_hash
from app.core.config import settings


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_create: RegisterRequest) -> UserResponse:
        # Vérification si l'email existe déjà
        existing_email = await self.get_user_by_email(user_create.email)
        if existing_email:
            raise ValueError("Email already registered")

        # Vérification si le nom d'utilisateur existe déjà
        existing_username = await self.get_user_by_username(user_create.username)
        if existing_username:
            raise ValueError("Username already taken")

        # Générer le full_username avec le domaine
        domain = settings.DOMAIN
        full_username = f"@{user_create.username}@{domain}"

        # Hachage du mot de passe
        hashed_password = get_password_hash(user_create.password)
        new_user = User(
            email=user_create.email,
            username=user_create.username,
            full_username=full_username,  # Ajout du full_username
            hashed_password=hashed_password,
            is_active=True
        )

        # Ajout du nouvel utilisateur à la session et commit
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        # Retourne l'utilisateur avec full_username
        return UserResponse(
            id=new_user.id,
            email=new_user.email,
            username=new_user.username,
            full_username=new_user.full_username  # Ajouter le full_username à la réponse
        )

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()
