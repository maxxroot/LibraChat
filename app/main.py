# app/main.py

import logging
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine
from contextlib import asynccontextmanager
from app.models import user, server, channel, message
from app.database import async_engine, Base
from app.core.config import settings
import uvicorn

logging.basicConfig(
    level=settings.LOG_LEVEL.upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger()
logger.setLevel(settings.LOG_LEVEL.upper())

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code de démarrage
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Base de données initialisée.")

    yield  # Point de suspension entre le démarrage et l'arrêt

    # Code de fermeture
    await async_engine.dispose()
    logger.info("Fermeture de la connexion à la base de données.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware pour capturer les erreurs et les requêtes
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Requête: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Réponse: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Erreur: {e}")
        raise e

from app.api.v1 import user, message, channel, server

app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(server.router, prefix="/api/v1/servers", tags=["servers"])
app.include_router(channel.router, prefix="/api/v1/channels", tags=["channels"])
app.include_router(message.router, prefix="/api/v1/messages", tags=["messages"])

if __name__ == "__main__":
    logger.info(f"Démarrage de l'application {settings.DOMAIN}")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, log_level=settings.LOG_LEVEL.lower(), reload=True)