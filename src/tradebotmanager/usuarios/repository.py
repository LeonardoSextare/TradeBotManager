from sqlalchemy.orm import Session
from typing import List, Optional
from .model import Usuario, TipoUsuario
from ..corretoras_usuarios.model import CorretoraUsuario


class UsuarioRepository:
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """
        Busca usuário por ID
        Args:
            usuario_id: ID do usuário
        """
        return self.sessao.query(Usuario).filter(Usuario.id == usuario_id).first()

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """
        Busca usuário por email
        Args:
            email: Email do usuário
        
        Para validar se email já existe, use: buscar_por_email(email) is not None
        """
        return self.sessao.query(Usuario).filter(Usuario.email == email).first()

    def listar_usuarios(self, ativo: Optional[bool] = True) -> List[Usuario]:
        """
        Lista usuários com filtro de status
        Args:
            ativo: True=só ativos, False=só inativos, None=todos
        """
        query = self.sessao.query(Usuario)
        
        if ativo is not None:
            query = query.filter(Usuario.ativo.is_(ativo))
        
        return query.all()

    def listar_admins(self, ativo: Optional[bool] = True) -> List[Usuario]:
        """
        Lista usuários administradores
        Args:
            ativo: True=só ativos, False=só inativos, None=todos
        """
        query = self.sessao.query(Usuario).filter(Usuario.tipo == TipoUsuario.ADMIN)
        
        if ativo is not None:
            query = query.filter(Usuario.ativo.is_(ativo))
        
        return query.all()

    def buscar_por_corretora(self, corretora_id: int, ativo: Optional[bool] = True) -> List[Usuario]:
        """
        Lista usuários que possuem conta em uma corretora específica
        Args:
            corretora_id: ID da corretora
            ativo: True=só ativos, False=só inativos, None=todos
        """
        query = self.sessao.query(Usuario)\
            .join(CorretoraUsuario)\
            .filter(CorretoraUsuario.corretora_id == corretora_id)
        
        if ativo is not None:
            query = query.filter(
                CorretoraUsuario.ativo.is_(ativo),
                Usuario.ativo.is_(ativo)
            )
        
        return query.all()

    def criar(self, usuario: Usuario) -> Usuario:
        """Cria novo usuário"""
        self.sessao.add(usuario)
        self.sessao.commit()
        self.sessao.refresh(usuario)
        return usuario

    def atualizar(self, usuario: Usuario) -> Usuario:
        """Atualiza usuário existente"""
        self.sessao.commit()
        self.sessao.refresh(usuario)
        return usuario

    def desativar(self, usuario_id: int) -> bool:
        """Soft delete - marca usuário como inativo"""
        usuario = self.buscar_por_id(usuario_id)
        if usuario:
            # Usar update query para evitar problemas de tipo
            self.sessao.query(Usuario)\
                .filter(Usuario.id == usuario_id)\
                .update({Usuario.ativo: False})
            self.sessao.commit()
            return True
        return False

    def ativar(self, usuario_id: int) -> bool:
        """Reativa usuário inativo"""
        # Busca usuário mesmo se inativo
        usuario = self.sessao.query(Usuario).filter(Usuario.id == usuario_id).first()
        if usuario:
            self.sessao.query(Usuario)\
                .filter(Usuario.id == usuario_id)\
                .update({Usuario.ativo: True})
            self.sessao.commit()
            return True
        return False