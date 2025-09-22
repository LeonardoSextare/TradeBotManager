from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import ModelBase


class CorretoraUsuario(ModelBase):
    __tablename__ = "corretoras_usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    corretora_id = Column(Integer, ForeignKey("corretoras.id"), nullable=False)
    login = Column(String(100), nullable=False)
    senha = Column(String(255), nullable=False)
    token_jwt = Column(String(500), nullable=True)
    api_token = Column(String(255), nullable=True) # Uso futuro
    ativo = Column(Boolean, default=True, nullable=False)
    
    # Relacionamentos
    dono_conta = relationship("Usuario", back_populates="contas_corretoras")
    corretora = relationship("Corretora", back_populates="contas_usuarios")
