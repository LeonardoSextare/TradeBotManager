from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from tradebotmanager.database import ModelBase


class Usuario(ModelBase):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    ativo = Column(Integer, default=True)

    # RELATIONSHIP: Um usuário pode ter várias corretoras
    # back_populates conecta com Corretora.usuario
    corretoras = relationship("Corretora", back_populates="usuario")
