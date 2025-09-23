from typing import List, Optional

from .model import Usuario, TipoUsuario
from .repository import UsuarioRepository

class UsuarioService:
    """
    Camada de serviço para operações relacionadas a usuários.
    """
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    def criar_usuario(self, nome: str, email: str, senha: str, tipo=None) -> Usuario:
        """Cria um novo usuário."""
        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha,
            tipo=tipo or TipoUsuario.USUARIO,
            ativo=True
        )
        return self.repository.criar(usuario)

    def buscar_por_id(self, usuario_id: int) -> Usuario:
        """Busca um usuário pelo ID. Lança ValueError se não encontrado."""
        usuario = self.repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError(f"Usuário com id {usuario_id} não encontrado.")
        
        return usuario

    def listar_usuarios(self, ativo: Optional[bool] = True) -> List[Usuario]:
        """Lista todos os usuários, podendo filtrar por ativos/inativos."""
        return self.repository.listar_usuarios(ativo=ativo)

    def atualizar_usuario(self, usuario_id: int, **dados) -> Usuario:
        """Atualiza dados de um usuário. Lança ValueError se não encontrado."""
        usuario = self.repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError(f"Usuário com id {usuario_id} não encontrado.")
        
        for campo, valor in dados.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)
        return self.repository.atualizar(usuario)

    def desativar_usuario(self, usuario_id: int) -> bool:
        """Marca o usuário como inativo (soft delete). Lança ValueError se não encontrado."""
        usuario = self.repository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError(f"Usuário com id {usuario_id} não encontrado.")
        
        return self.repository.desativar(usuario_id)
