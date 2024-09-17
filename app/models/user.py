# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    public_key = Column(String, nullable=True)
    private_key = Column(String, nullable=True)

    owned_servers = relationship("Server", back_populates="owner")  # Propriétaire des serveurs
    servers = relationship("Server", secondary="server_members", back_populates="members")  # Membre des serveurs

# Ensure 'Server' is imported after it is fully defined
from app.models.server import Server  # Import this after class definition to avoid circular import issues
