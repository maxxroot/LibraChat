# app/database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

Base = declarative_base()

# Création de l'engine pour les requêtes asynchrones
async_engine = create_async_engine(settings.ASYNC_DATABASE_URL, future=True, echo=True)

# Configuration de la session asynchrone
async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Adding a check to validate the connection to the database at startup
async def validate_database_connection():
    async with async_engine.begin() as conn:
        await conn.run_sync(lambda: conn.connection().ping())

