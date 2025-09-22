from typing import Any, List, Optional
from .client import ClienteOptionMarket

class OptionMarketRepository:
    """
    Repository para operações de copy-trade na OptionMarket via API externa.
    Depende de ClienteOptionMarket para autenticação e requisições.
    """
    def __init__(self, client: ClienteOptionMarket):
        self.client = client

    def seguir_bot(self, profile_id: str, max_balance_to_use: float) -> str:
        """
        Segue um trader criando um copy-trade. Retorna o id da assinatura criada.
        """
        body = {
            "maxBalanceToUse": max_balance_to_use,
            "traderUserId": profile_id,
            "stopLoss": 1000000,
        }
        try:
            resp = self.client.post("/copy-trade", dados=body)
            return resp["id"]
        except Exception as exc:
            msg = str(exc)
            raise RuntimeError(f"Erro ao seguir bot: {msg}")

    def deixar_de_seguir_bot(self, broker_copy_id: str) -> bool:
        """
        Cancela (unfollow) um copy-trade e verifica se ficou inativo.
        """
        path = f"/copy-trade/{broker_copy_id}/inactive"
        
        try:
            self.client.patch(path, dados={})
        except Exception as exc:
            raise RuntimeError(f"Erro ao deixar de seguir bot: {exc}")
        
        # Verifica se ficou inativo
        bots = self.listar_bots(ativo=False)
        for bot in bots:
            if bot["id"] == broker_copy_id:
                return not bot.get("active", True)
        return False

    def listar_bots(self, ativo: bool = True) -> List[dict]:
        """
        Lista bots filtrando por ativo/inativo.
        """
        ativo_str = "true" if ativo else "false"
        path = f"/copy-trade?page=1&pageSize=100&active={ativo_str}&orderBy=updatedAt&orderDirection=DESC"
        try:
            resp = self.client.get(path)
            return resp["data"]
        except Exception as exc:
            msg = str(exc)
            raise RuntimeError(f"Erro ao listar bots: {msg}")

    def atualizar_status_aprovado(self, broker_copy_id: str, tentativas: int = 3) -> bool:
        """
        Garante que o copy-trade fique com status APPROVED, tentando refuse/approve.
        """
        if tentativas < 1:
            tentativas = 1

        refuse_path = f"/copy-trade/{broker_copy_id}/refuse-follower"
        approve_path = f"/copy-trade/{broker_copy_id}/approve-follower"
        for _ in range(tentativas):
            try:
                self.client.patch(refuse_path, dados={})
            except Exception as exc:
                msg = str(exc)
                if "already refused" not in msg.lower():
                    raise RuntimeError(f"Erro ao recusar bot: {msg}")
                
            try:
                self.client.patch(approve_path, dados={})
            except Exception as exc:
                msg = str(exc)
                if "already approved" not in msg.lower():
                    raise RuntimeError(f"Erro ao aprovar bot: {msg}")
            bots = self.listar_bots(ativo=True)
            
            for bot in bots:
                if bot["id"] == broker_copy_id and bot.get("status") == "APPROVED":
                    return True
        return False
