# app/services/message.py

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message
from app.schemas.message import MessageCreate

class MessageService:
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    async def create_message(db: AsyncSession, message: MessageCreate):
        db_message = Message(**message.dict())
        db.add(db_message)
        await db.commit()
        await db.refresh(db_message)
        return db_message

    @staticmethod
    async def get_message(db: AsyncSession, message_id: int):
        return await db.get(Message, message_id)

    @staticmethod
    async def get_messages_for_channel(db: AsyncSession, channel_id: int):
        result = await db.execute(select(Message).filter(Message.channel_id == channel_id))
        return result.scalars().all()
