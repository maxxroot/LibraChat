# app/schemas/message.py

from pydantic import BaseModel

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    channel_id: int

class MessageResponse(MessageBase):
    id: int
    sender_id: int

    class Config:
        from_attributes = True
