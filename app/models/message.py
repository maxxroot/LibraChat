# app/models/message.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    channel_id = Column(Integer, ForeignKey('channels.id'))

    # Référence à la classe 'Channel' sous forme de chaîne pour éviter les problèmes d'importation circulaire
    channel = relationship("Channel", back_populates="messages")

class PrivateMessage(Base):
    __tablename__ = "private_messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    encrypted_message = Column(String, nullable=False)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
