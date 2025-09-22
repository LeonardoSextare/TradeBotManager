from sqlalchemy.orm import Session
from typing import List, Optional
from .model import Corretora


class CorretoraRepository:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def buscar_por_id(self, corretora_id: int) -> Optional[Corretora]:
        """
        Busca corretora por ID
        Args:
            corretora_id: ID da corretora
        """
        return self.sessao.query(Corretora).filter(Corretora.id == corretora_id).first()

    def buscar_por_nome(self, nome: str) -> Optional[Corretora]:
        """
        Busca corretora por nome
        Args:
            nome: Nome da corretora
        
        Para validar se nome já existe, use: buscar_por_nome(nome) is not None
        """
        return self.sessao.query(Corretora).filter(Corretora.nome == nome).first()

    def listar_corretoras(self, ativo: Optional[bool] = True) -> List[Corretora]:
        """
        Lista corretoras com filtro de status
        Args:
            ativo: True=só ativas, False=só inativas, None=todas
        """
        query = self.sessao.query(Corretora)
        
        if ativo is not None:
            query = query.filter(Corretora.ativo.is_(ativo))
        
        return query.all()

    def criar(self, corretora: Corretora) -> Corretora:
        """Cria nova corretora"""
        self.sessao.add(corretora)
        self.sessao.commit()
        self.sessao.refresh(corretora)
        return corretora

    def atualizar(self, corretora: Corretora) -> Corretora:
        """Atualiza corretora existente"""
        self.sessao.commit()
        self.sessao.refresh(corretora)
        return corretora

    def desativar(self, corretora_id: int) -> bool:
        """Soft delete - marca corretora como inativa"""
        corretora = self.buscar_por_id(corretora_id)
        if corretora:
            # Usar update query para evitar problemas de tipo
            self.sessao.query(Corretora)\
                .filter(Corretora.id == corretora_id)\
                .update({Corretora.ativo: False})
            self.sessao.commit()
            return True
        return False

    def ativar(self, corretora_id: int) -> bool:
        """Reativa corretora inativa"""
        # Busca corretora mesmo se inativa
        corretora = self.sessao.query(Corretora).filter(Corretora.id == corretora_id).first()
        if corretora:
            self.sessao.query(Corretora)\
                .filter(Corretora.id == corretora_id)\
                .update({Corretora.ativo: True})
            self.sessao.commit()
            return True
        return False
