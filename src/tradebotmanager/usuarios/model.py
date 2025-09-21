from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import ModelBase


class Usuario(ModelBase):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    corretoras = relationship(
        "CorretoraUsuario", back_populates="usuario", cascade="all, delete-orphan"
    )
    bots_op_mkt = relationship(
        "BotUsuarioOpMkt", back_populates="usuario", cascade="all, delete-orphan"
    )
