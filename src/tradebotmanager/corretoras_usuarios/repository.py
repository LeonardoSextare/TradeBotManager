from sqlalchemy.orm import Session
from typing import List, Optional
from .model import CorretoraUsuario


class CorretoraUsuarioRepository:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def buscar_por_id(self, conta_id: int) -> Optional[CorretoraUsuario]:
        """
        Busca conta por ID
        Args:
            conta_id: ID da conta
        """
        return self.sessao.query(CorretoraUsuario).filter(CorretoraUsuario.id == conta_id).first()

    def buscar_por_usuario_e_corretora(self, usuario_id: int, corretora_id: int) -> Optional[CorretoraUsuario]:
        """
        Busca conta específica de um usuário em uma corretora
        Args:
            usuario_id: ID do usuário
            corretora_id: ID da corretora
        """
        return self.sessao.query(CorretoraUsuario).filter(
            CorretoraUsuario.usuario_id == usuario_id,
            CorretoraUsuario.corretora_id == corretora_id
        ).first()

    def listar_por_usuario(self, usuario_id: int, ativo: Optional[bool] = True) -> List[CorretoraUsuario]:
        """
        Lista contas de um usuário
        Args:
            usuario_id: ID do usuário
            ativo: True=só ativas, False=só inativas, None=todas
        """
        query = self.sessao.query(CorretoraUsuario).filter(CorretoraUsuario.usuario_id == usuario_id)
        
        if ativo is not None:
            query = query.filter(CorretoraUsuario.ativo.is_(ativo))
        
        return query.all()

    def listar_por_corretora(self, corretora_id: int, ativo: Optional[bool] = True) -> List[CorretoraUsuario]:
        """
        Lista contas de uma corretora
        Args:
            corretora_id: ID da corretora
            ativo: True=só ativas, False=só inativas, None=todas
        """
        query = self.sessao.query(CorretoraUsuario).filter(CorretoraUsuario.corretora_id == corretora_id)
        
        if ativo is not None:
            query = query.filter(CorretoraUsuario.ativo.is_(ativo))
        
        return query.all()

    def buscar_por_login(self, corretora_id: int, login: str) -> Optional[CorretoraUsuario]:
        """
        Busca conta por login específico na corretora
        Args:
            corretora_id: ID da corretora
            login: Login da conta
        
        Para validar se login já existe na corretora, use: buscar_por_login(corretora_id, login) is not None
        """
        return self.sessao.query(CorretoraUsuario).filter(
            CorretoraUsuario.corretora_id == corretora_id,
            CorretoraUsuario.login == login
        ).first()

    def criar(self, conta: CorretoraUsuario) -> CorretoraUsuario:
        """Cria nova conta"""
        self.sessao.add(conta)
        self.sessao.commit()
        self.sessao.refresh(conta)
        return conta

    def atualizar(self, conta: CorretoraUsuario) -> CorretoraUsuario:
        """Atualiza conta existente"""
        self.sessao.commit()
        self.sessao.refresh(conta)
        return conta

    def desativar(self, conta_id: int) -> bool:
        """Soft delete - marca conta como inativa"""
        conta = self.buscar_por_id(conta_id)
        if conta:
            # Usar update query para evitar problemas de tipo
            self.sessao.query(CorretoraUsuario)\
                .filter(CorretoraUsuario.id == conta_id)\
                .update({CorretoraUsuario.ativo: False})
            self.sessao.commit()
            return True
        return False

    def ativar(self, conta_id: int) -> bool:
        """Reativa conta inativa"""
        # Busca conta mesmo se inativa
        conta = self.sessao.query(CorretoraUsuario).filter(CorretoraUsuario.id == conta_id).first()
        if conta:
            self.sessao.query(CorretoraUsuario)\
                .filter(CorretoraUsuario.id == conta_id)\
                .update({CorretoraUsuario.ativo: True})
            self.sessao.commit()
            return True
        return False