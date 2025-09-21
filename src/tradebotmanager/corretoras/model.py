from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import ModelBase


class Corretora(ModelBase):
    __tablename__ = "corretoras"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)
    
    usuarios = relationship("CorretoraUsuario", back_populates="corretora")
    bots = relationship("BotOptionMarket", back_populates="corretora")
