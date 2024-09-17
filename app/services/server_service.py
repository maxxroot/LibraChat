# app/services/server_service.py

from app.models.server import Server
from app.models.channel import Channel
from app.schemas.server import ServerCreate
from sqlalchemy.ext.asyncio import AsyncSession

class ServerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_server(self, server_create: ServerCreate, owner_id: int):
        # Create the server
        new_server = Server(
            name=server_create.name,
            description=server_create.description,
            owner_id=owner_id
        )
        self.session.add(new_server)
        await self.session.commit()
        await self.session.refresh(new_server)

        # Create a default "général" channel for the new server
        general_channel = Channel(
            name="général",
            server_id=new_server.id,
            owner_id=owner_id
        )
        self.session.add(general_channel)
        await self.session.commit()

        return new_server
