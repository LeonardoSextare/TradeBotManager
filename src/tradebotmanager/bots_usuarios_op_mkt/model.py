from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import ModelBase


class BotUsuarioOpMkt(ModelBase):
    __tablename__ = "bots_usuarios_op_mkt"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    bot_option_market_id = Column(Integer, ForeignKey("bots_option_market.id"), nullable=False)
    copy_trade_id = Column(String(100), nullable=True)
    ativo = Column(Boolean, default=True, nullable=False)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="bots")
    bot_option_market = relationship("BotOptionMarket", back_populates="usuarios")