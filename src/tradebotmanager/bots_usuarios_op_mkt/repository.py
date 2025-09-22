from sqlalchemy.orm import Session
from typing import List, Optional
from .model import BotUsuarioOpMkt


class BotUsuarioOpMktRepository:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def buscar_por_id(self, associacao_id: int) -> Optional[BotUsuarioOpMkt]:
        """
        Busca associação por ID
        Args:
            associacao_id: ID da associação
        """
        return self.sessao.query(BotUsuarioOpMkt).filter(BotUsuarioOpMkt.id == associacao_id).first()

    def buscar_por_usuario_e_bot(self, usuario_id: int, bot_id: int) -> Optional[BotUsuarioOpMkt]:
        """
        Busca associação específica entre usuário e bot
        Args:
            usuario_id: ID do usuário
            bot_id: ID do bot
        """
        return self.sessao.query(BotUsuarioOpMkt).filter(
            BotUsuarioOpMkt.usuario_id == usuario_id,
            BotUsuarioOpMkt.bot_option_market_id == bot_id
        ).first()

    def buscar_por_copy_trade_id(self, copy_trade_id: str) -> Optional[BotUsuarioOpMkt]:
        """
        Busca associação por ID do copy trade
        Args:
            copy_trade_id: ID do copy trade
        
        Para validar se copy_trade_id já existe, use: buscar_por_copy_trade_id(copy_trade_id) is not None
        """
        return self.sessao.query(BotUsuarioOpMkt).filter(BotUsuarioOpMkt.copy_trade_id == copy_trade_id).first()

    def listar_por_usuario(self, usuario_id: int, ativo: Optional[bool] = True) -> List[BotUsuarioOpMkt]:
        """
        Lista associações de um usuário
        Args:
            usuario_id: ID do usuário
            ativo: True=só ativos, False=só inativos, None=todos
        """
        query = self.sessao.query(BotUsuarioOpMkt).filter(BotUsuarioOpMkt.usuario_id == usuario_id)
        
        if ativo is not None:
            query = query.filter(BotUsuarioOpMkt.ativo.is_(ativo))
        
        return query.all()

    def listar_por_bot(self, bot_id: int, ativo: Optional[bool] = True) -> List[BotUsuarioOpMkt]:
        """
        Lista associações de um bot
        Args:
            bot_id: ID do bot
            ativo: True=só ativos, False=só inativos, None=todos
        """
        query = self.sessao.query(BotUsuarioOpMkt).filter(BotUsuarioOpMkt.bot_option_market_id == bot_id)
        
        if ativo is not None:
            query = query.filter(BotUsuarioOpMkt.ativo.is_(ativo))
        
        return query.all()

    def listar_por_corretora(self, corretora_id: int, ativo: Optional[bool] = True) -> List[BotUsuarioOpMkt]:
        """
        Lista associações de bots de uma corretora específica
        Args:
            corretora_id: ID da corretora
            ativo: True=só ativos, False=só inativos, None=todos
        """
        from ..bots_option_market.model import BotOptionMarket
        
        query = self.sessao.query(BotUsuarioOpMkt)\
            .join(BotOptionMarket)\
            .filter(BotOptionMarket.corretora_id == corretora_id)
        
        if ativo is not None:
            query = query.filter(
                BotOptionMarket.ativo.is_(ativo),
                BotUsuarioOpMkt.ativo.is_(ativo)
            )
        
        return query.all()

    def criar(self, associacao: BotUsuarioOpMkt) -> BotUsuarioOpMkt:
        """Cria nova associação"""
        self.sessao.add(associacao)
        self.sessao.commit()
        self.sessao.refresh(associacao)
        return associacao

    def atualizar(self, associacao: BotUsuarioOpMkt) -> BotUsuarioOpMkt:
        """Atualiza associação existente"""
        self.sessao.commit()
        self.sessao.refresh(associacao)
        return associacao

    def desativar(self, associacao_id: int) -> bool:
        """Soft delete - marca associação como inativa"""
        associacao = self.buscar_por_id(associacao_id)
        if associacao:
            # Usar update query para evitar problemas de tipo
            self.sessao.query(BotUsuarioOpMkt)\
                .filter(BotUsuarioOpMkt.id == associacao_id)\
                .update({BotUsuarioOpMkt.ativo: False})
            self.sessao.commit()
            return True
        return False

    def ativar(self, associacao_id: int) -> bool:
        """Reativa associação inativa"""
        # Busca associação mesmo se inativa
        associacao = self.sessao.query(BotUsuarioOpMkt).filter(BotUsuarioOpMkt.id == associacao_id).first()
        if associacao:
            self.sessao.query(BotUsuarioOpMkt)\
                .filter(BotUsuarioOpMkt.id == associacao_id)\
                .update({BotUsuarioOpMkt.ativo: True})
            self.sessao.commit()
            return True
        return False