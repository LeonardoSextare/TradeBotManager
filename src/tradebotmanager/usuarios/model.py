from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from database import ModelBase
import enum


class TipoUsuario(enum.Enum):
    """Tipos de usuário disponíveis no sistema"""
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"


class Usuario(ModelBase):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoUsuario), nullable=False, default=TipoUsuario.USUARIO)
    ativo = Column(Boolean, default=True, nullable=False)

    # Relacionamentos
    contas_corretoras = relationship(
        "CorretoraUsuario", back_populates="dono_conta", cascade="all, delete-orphan"
    )
    bots_option_market = relationship(
        "BotUsuarioOpMkt", back_populates="usuario", cascade="all, delete-orphan"
    )
