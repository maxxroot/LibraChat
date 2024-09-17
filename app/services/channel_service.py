# app/services/channel_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Channel, Server
from app.schemas.channel import ChannelCreate

class ChannelService:
    def __init__(self, session: AsyncSession):
        self.session = session

async def create_channel(server_id: int, channel_data: ChannelCreate, db: AsyncSession):
    # Vérifier si le serveur existe
    result = await db.execute(select(Server).filter(Server.id == server_id))
    server = result.scalars().first()

    if not server:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Le serveur spécifié n'existe pas."
        )

    # Créer le nouveau canal
    new_channel = Channel(
        name=channel_data.name,
        description=channel_data.description,
        server_id=server_id
    )

    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)  # Rafraîchir l'instance avec l'ID généré
    return new_channel