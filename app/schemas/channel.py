# app/schemas/channel.py

from pydantic import BaseModel

class ChannelCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True

