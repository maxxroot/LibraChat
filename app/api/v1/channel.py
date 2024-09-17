# app/api/v1/channel.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.channel import ChannelCreate
from app.models.channel import Channel
from app.models.message import Message
from app.dependencies import get_async_session, get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/")
async def list_channels(server_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Channel).filter(Channel.server_id == server_id))
    channels = result.scalars().all()
    if not channels:
        raise HTTPException(status_code=404, detail="No channels found for this server")
    return channels

@router.post("/")
async def create_channel(server_id: int, channel_data: ChannelCreate, db: AsyncSession = Depends(get_async_session)):
    new_channel = Channel(server_id=server_id, **channel_data.dict())
    db.add(new_channel)
    await db.commit()
    await db.refresh(new_channel)

    welcome_message = Message(content="Bienvenue dans le canal", channel_id=new_channel.id)
    db.add(welcome_message)
    await db.commit()

    return new_channel


@router.get("/{channel_id}/messages")
async def list_messages(channel_id: int, current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_async_session)):
    # Vérifier si l'utilisateur a accès au channel
    result = await db.execute(
        select(Channel).filter(Channel.id == channel_id).filter(Channel.server.users.contains(current_user)))
    channel = result.scalars().first()
    if not channel:
        raise HTTPException(status_code=403, detail="Vous n'avez pas accès à ce channel")

    # Récupérer les messages du channel
    messages = await db.execute(select(Message).filter(Message.channel_id == channel_id))
    return messages.scalars().all()