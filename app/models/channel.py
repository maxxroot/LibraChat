# app/models/channel.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    server_id = Column(Integer, ForeignKey('servers.id'))

    # Correction ici : back_populates="channels" et non "channel"
    server = relationship("Server", back_populates="channels")
    messages = relationship("Message", back_populates="channel")
