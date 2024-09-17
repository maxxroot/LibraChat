# app/api/v1/server.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_async_session
from app.models.server import Server
from app.schemas.server import ServerCreate, ServerResponse
from app.models.user import User
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=ServerResponse)
async def create_server(
    server_data: ServerCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    async with session.begin():
        # Vérifier si un serveur avec le même nom existe déjà
        result = await session.execute(
            select(Server).where(Server.name == server_data.name)
        )
        existing_server = result.scalars().first()
        if existing_server:
            raise HTTPException(status_code=400, detail="Server name already exists")

        # Créer un nouveau serveur
        new_server = Server(
            name=server_data.name,
            description=server_data.description,
            owner_id=current_user.id
        )
        session.add(new_server)
        await session.commit()
        await session.refresh(new_server)

    return new_server

@router.get("/")
async def list_servers(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Server).filter(Server.users.contains(current_user)))
    servers = result.scalars().all()
    if not servers:
        raise HTTPException(status_code=404, detail="Aucun serveur disponible pour cet utilisateur")
    return servers

@router.get("/{server_id}", response_model=ServerResponse)
async def get_server(
    server_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    async with session.begin():
        result = await session.execute(select(Server).where(Server.id == server_id))
        server = result.scalars().first()
        if not server:
            raise HTTPException(status_code=404, detail="Server not found")
        if server.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to view this server")
    return server
