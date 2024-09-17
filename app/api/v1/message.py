# app/api/v1/message.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.crypto import encrypt_message, decrypt_message
from app.models.user import User
from app.models.message import Message
from app.dependencies import get_current_user, get_async_session

router = APIRouter()

@router.get("/{channel_id}/messages")
async def get_messages(channel_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Message).filter(Message.channel_id == channel_id))
    messages = result.scalars().all()
    if not messages:
        return []
    return messages

@router.post("/send_message/")
async def send_message(
    recipient_id: int,
    message: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    recipient = await session.get(User, recipient_id)
    if not recipient or not recipient.public_key:
        raise HTTPException(status_code=404, detail="Recipient not found or has no public key")

    iv, encrypted_aes_key, ciphertext = encrypt_message(recipient.public_key, message)

    # Stockez le message chiffré dans la base de données (non inclus ici)
    return {"iv": iv, "key": encrypted_aes_key, "message": ciphertext}

@router.post("/read_message/")
async def read_message(
    iv: bytes,
    encrypted_aes_key: bytes,
    ciphertext: bytes,
    current_user: User = Depends(get_current_user)
):
    if not current_user.private_key:
        raise HTTPException(status_code=404, detail="User has no private key")

    message = decrypt_message(current_user.private_key, iv, encrypted_aes_key, ciphertext)

    return {"message": message}
