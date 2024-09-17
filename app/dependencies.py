# app/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt
from app.database import get_async_session, async_session
from app.models.user import User
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")

async def get_current_user(
        session: AsyncSession = Depends(get_async_session),
        token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Décodage du token JWT avec full_username dans le champ "sub"
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        full_username: str = payload.get("sub")
        if full_username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Recherche de l'utilisateur par full_username
    result = await session.execute(select(User).where(User.full_username == full_username))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user

async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
