from typing import List, Optional
from .model import Corretora
from .repository import CorretoraRepository

class CorretoraService:
    """
    Camada de serviço para operações relacionadas a corretoras.
    """
    def __init__(self, repository: CorretoraRepository):
        self.repository = repository

    def criar_corretora(self, nome: str) -> Corretora:
        """Cria uma nova corretora."""
        corretora = Corretora(nome=nome, ativo=True)
        return self.repository.criar(corretora)

    def buscar_por_id(self, corretora_id: int) -> Corretora:
        """Busca uma corretora pelo ID. Lança ValueError se não encontrada."""
        corretora = self.repository.buscar_por_id(corretora_id)
        if not corretora:
            raise ValueError(f"Corretora com id {corretora_id} não encontrada.")
        
        return corretora

    def listar_corretoras(self, ativo: Optional[bool] = True) -> List[Corretora]:
        """Lista todas as corretoras, podendo filtrar por ativas/inativas."""
        return self.repository.listar_corretoras(ativo=ativo)

    def atualizar_corretora(self, corretora_id: int, **dados) -> Corretora:
        """Atualiza dados de uma corretora. Lança ValueError se não encontrada."""
        corretora = self.repository.buscar_por_id(corretora_id)
        if not corretora:
            raise ValueError(f"Corretora com id {corretora_id} não encontrada.")
        
        for campo, valor in dados.items():
            if hasattr(corretora, campo):
                setattr(corretora, campo, valor)
                
        return self.repository.atualizar(corretora)

    def desativar_corretora(self, corretora_id: int) -> bool:
        """Marca a corretora como inativa (soft delete). Lança ValueError se não encontrada."""
        corretora = self.repository.buscar_por_id(corretora_id)
        if not corretora:
            raise ValueError(f"Corretora com id {corretora_id} não encontrada.")
        
        return self.repository.desativar(corretora_id)
