from sqlalchemy.orm import Session
from typing import List, Optional
from .model import BotOptionMarket


class BotOptionMarketRepository:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def buscar_por_id(self, bot_id: int) -> Optional[BotOptionMarket]:
        """
        Busca bot por ID
        Args:
            bot_id: ID do bot
        """
        return self.sessao.query(BotOptionMarket).filter(BotOptionMarket.id == bot_id).first()

    def buscar_por_id_perfil(self, id_perfil: str) -> Optional[BotOptionMarket]:
        """
        Busca bot por ID do perfil na OptionMarket
        Args:
            id_perfil: ID do perfil
        
        Para validar se id_perfil já existe, use: buscar_por_id_perfil(id_perfil) is not None
        """
        return self.sessao.query(BotOptionMarket).filter(BotOptionMarket.id_perfil == id_perfil).first()

    def buscar_por_nome(self, nome: str) -> Optional[BotOptionMarket]:
        """
        Busca bot por nome
        Args:
            nome: Nome do bot
        
        Para validar se nome já existe, use: buscar_por_nome(nome) is not None
        """
        return self.sessao.query(BotOptionMarket).filter(BotOptionMarket.nome == nome).first()

    def listar_bots(self, ativo: Optional[bool] = True) -> List[BotOptionMarket]:
        """
        Lista bots com filtro de status
        Args:
            ativo: True=só ativos, False=só inativos, None=todos
        """
        query = self.sessao.query(BotOptionMarket)
        
        if ativo is not None:
            query = query.filter(BotOptionMarket.ativo.is_(ativo))
        
        return query.all()

    def listar_por_corretora(self, corretora_id: int, ativo: Optional[bool] = True) -> List[BotOptionMarket]:
        """
        Lista bots de uma corretora específica
        Args:
            corretora_id: ID da corretora
            ativo: True=só ativos, False=só inativos, None=todos
        """
        query = self.sessao.query(BotOptionMarket).filter(BotOptionMarket.corretora_id == corretora_id)
        
        if ativo is not None:
            query = query.filter(BotOptionMarket.ativo.is_(ativo))
        
        return query.all()
    
    def criar(self, bot: BotOptionMarket) -> BotOptionMarket:
        """Cria novo bot"""
        self.sessao.add(bot)
        self.sessao.commit()
        self.sessao.refresh(bot)
        return bot

    def atualizar(self, bot: BotOptionMarket) -> BotOptionMarket:
        """Atualiza bot existente"""
        self.sessao.commit()
        self.sessao.refresh(bot)
        return bot

    def desativar(self, bot_id: int) -> bool:
        """Soft delete - marca bot como inativo"""
        bot = self.buscar_por_id(bot_id)
        if bot:
            # Usar update query para evitar problemas de tipo
            self.sessao.query(BotOptionMarket)\
                .filter(BotOptionMarket.id == bot_id)\
                .update({BotOptionMarket.ativo: False})
            self.sessao.commit()
            return True
        return False

    def ativar(self, bot_id: int) -> bool:
        """Reativa bot inativo"""
        # Busca bot mesmo se inativo
        bot = self.sessao.query(BotOptionMarket).filter(BotOptionMarket.id == bot_id).first()
        if bot:
            self.sessao.query(BotOptionMarket)\
                .filter(BotOptionMarket.id == bot_id)\
                .update({BotOptionMarket.ativo: True})
            self.sessao.commit()
            return True
        return False