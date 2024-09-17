# app/models/server.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# Table de liaison pour les membres des serveurs
server_members = Table(
    "server_members",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("server_id", ForeignKey("servers.id"), primary_key=True)
)

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="owned_servers")
    members = relationship("User", secondary=server_members, back_populates="servers")  # Ajoute la relation many-to-many
    channels = relationship("Channel", back_populates="server")
