from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import ModelBase


class BotOptionMarket(ModelBase):
    __tablename__ = "bots_option_market"

    id = Column(Integer, primary_key=True, index=True)
    id_perfil = Column(String(100), nullable=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(500), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    
    # Relacionamento com corretora - um bot pertence a uma corretora
    corretora_id = Column(Integer, ForeignKey("corretoras.id"), nullable=False)
    corretora = relationship("Corretora", back_populates="bots")
