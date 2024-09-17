# app/schemas/sever.py

from pydantic import BaseModel

class ServerBase(BaseModel):
    name: str
    description: str | None = None

class ServerCreate(BaseModel):
    name: str
    description: str

    def __init__(self, **data):
        super().__init__(**data)

class ServerResponse(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int

    class Config:
        from_attributes = True
