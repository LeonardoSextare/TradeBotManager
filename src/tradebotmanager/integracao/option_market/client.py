import cloudscraper
import json
import base64
import time
from typing import Dict, Optional, Any


class ClienteOptionMarket:
    """
    Cliente para comunicação com a API da OptionMarket usando cloudscraper
    para bypass de proteções anti-bot
    """
    
    URL_BASE = "https://broker-api.mybroker.dev"
    
    CABECALHOS_FIXOS: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "pt-BR,en-US;q=0.8,pt;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, zstd",
        "Origin": "https://broker.option.market",
        "DNT": "1",
        "Host": "broker-api.mybroker.dev",
        "Connection": "keep-alive",
        "Referer": "https://broker.option.market/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "TE": "trailers",
        "x-tenant-id": "01HZTB9FAN88DFM3T589J4FW17",
    }
    
    def __init__(self, email: str, senha: str, token: Optional[str] = None):
        """
        Inicializa o cliente da OptionMarket e valida/gera token automaticamente
        
        Args:
            email: Email para autenticação (obrigatório)
            senha: Senha para autenticação (obrigatório)
            token: Token existente (opcional). Se fornecido, será validado primeiro
            
        Raises:
            ValueError: Se credenciais não fornecidas ou autenticação falhar
        """
        if not email or not senha:
            raise ValueError("Email e senha são obrigatórios")
            
        self.sessao = cloudscraper.create_scraper()
        self.token: Optional[str] = token
        self.email = email
        self.senha = senha
        self.autenticado = False
    
        self.sessao.headers.update(self.CABECALHOS_FIXOS)
        
        self._validar_sessao()
    
    def _validar_sessao(self) -> None:
        """
        Valida o token JWT verificando a claim 'exp'.
        Se token está ausente, malformado ou expirado, gera um novo token.
        """
        token = self.token
        
        if not token:
            self._gerar_token()
            return
        
        try:
            # JWT format: header.payload.signature
            partes = token.split(".")
            if len(partes) < 2:
                # malformado
                self._gerar_token()
                return
            
            payload_b64 = partes[1]
            # Adiciona padding necessário para decodificação base64
            padding = "=" * (-len(payload_b64) % 4)
            payload_bytes = base64.urlsafe_b64decode(payload_b64 + padding)
            payload = json.loads(payload_bytes.decode("utf-8"))
            
            exp = payload.get("exp")
            if exp is None:
                self._gerar_token()
                return
            
            agora = int(time.time())
            # exp está em segundos desde epoch
            if agora < int(exp):
                # ainda válido
                self.autenticado = True
                return
            
            # expirado
            self._gerar_token()
            return
            
        except Exception:
            # qualquer erro ao analisar/validar -> renovar token
            self._gerar_token()
            return
    
    def _gerar_token(self) -> None:
        """
        Autentica usando as credenciais e armazena o bearer token.
        
        O método envia um JSON body como:
        {"tenantId":..., "email":..., "password":..., "agentNavigator":..., "recaptchaToken":...}
        
        Em caso de sucesso, a resposta JSON deve conter a chave 'token'.
        Em caso de falha, uma ValueError é levantada.
        """
        tenant_id = self.CABECALHOS_FIXOS.get("x-tenant-id")
        agent_navigator = self.CABECALHOS_FIXOS.get("User-Agent")
        
        corpo_requisicao = {
            "tenantId": tenant_id,
            "email": self.email,
            "password": self.senha,
            "agentNavigator": agent_navigator,
            "recaptchaToken": "bypass-2",
        }
        
        try:
            # Prepara headers com x-timestamp para requisição de login
            cabecalhos_login = self._preparar_cabecalhos()
            
            resposta = self.sessao.post(
                f"{self.URL_BASE}/auth/login",
                json=corpo_requisicao,
                headers=cabecalhos_login,
                timeout=10
            )
            dados = resposta.json()
            
            resposta.raise_for_status()
            
            token = dados["token"]
            self.token = token
            self.autenticado = True
            
        except Exception as e:
            try:
                mensagem = dados["data"]["message"]
                raise ValueError(f"Erro na autenticação: {mensagem}")
            except (KeyError, NameError):
                raise ValueError(f"Erro na autenticação: {e}")
    
    def _preparar_cabecalhos(self, cabecalhos: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        Prepara headers para requisição, adicionando timestamp e token (se disponível)
        
        Args:
            cabecalhos: Headers adicionais
            
        Returns:
            Headers completos para a requisição
        """
        # Garante que CABECALHOS_FIXOS têm precedência
        hdrs = {**(cabecalhos or {}), **self.CABECALHOS_FIXOS}
        hdrs["x-timestamp"] = str(int(time.time() * 1000))
        
        # Adiciona Authorization apenas se token já existir (para requisições autenticadas)
        if self.token:
            hdrs["Authorization"] = f"Bearer {self.token}"
            
        return hdrs
    
    def _fazer_requisicao(
        self, 
        metodo: str, 
        endpoint: str, 
        cabecalhos: Optional[Dict[str, str]] = None,
        dados_json: Optional[Dict[str, Any]] = None,
        parametros: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executa requisição HTTP com tratamento de erros
        
        Args:
            metodo: Método HTTP (GET, POST, etc.)
            endpoint: Endpoint da API (ex: /api/bots)
            cabecalhos: Headers adicionais
            dados_json: Dados JSON para POST/PUT
            parametros: Parâmetros de query string
            
        Returns:
            Resposta da API em formato dict
            
        Raises:
            ConnectionError: Erro de conexão
            ValueError: Erro de resposta da API
        """
        url = f"{self.URL_BASE}{endpoint}"
        cabecalhos_preparados = self._preparar_cabecalhos(cabecalhos)
        
        try:
            resposta = self.sessao.request(
                method=metodo,
                url=url,
                headers=cabecalhos_preparados,
                json=dados_json,
                params=parametros,
                timeout=30
            )
            
            resposta.raise_for_status()
            
            return resposta.json()
                
        except cloudscraper.exceptions.CloudflareChallengeError as e:
            raise ConnectionError(f"Cloudflare challenge falhou: {e}")
        except Exception as e:
            raise ConnectionError(f"Erro na requisição: {e}")
    
    def get(
        self, 
        endpoint: str, 
        parametros: Optional[Dict[str, Any]] = None,
        cabecalhos: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Executa requisição GET
        
        Args:
            endpoint: Endpoint da API
            parametros: Parâmetros de query
            cabecalhos: Headers adicionais
            
        Returns:
            Resposta da API
        """
        return self._fazer_requisicao("GET", endpoint, cabecalhos=cabecalhos, parametros=parametros)
    
    def post(
        self, 
        endpoint: str, 
        dados: Optional[Dict[str, Any]] = None,
        cabecalhos: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Executa requisição POST
        
        Args:
            endpoint: Endpoint da API
            dados: Dados para enviar
            cabecalhos: Headers adicionais
            
        Returns:
            Resposta da API
        """
        return self._fazer_requisicao("POST", endpoint, cabecalhos=cabecalhos, dados_json=dados)
    
    def patch(
        self, 
        endpoint: str, 
        dados: Optional[Dict[str, Any]] = None,
        cabecalhos: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Executa requisição PATCH
        
        Args:
            endpoint: Endpoint da API
            dados: Dados para enviar
            cabecalhos: Headers adicionais
            
        Returns:
            Resposta da API
        """
        return self._fazer_requisicao("PATCH", endpoint, cabecalhos=cabecalhos, dados_json=dados)
    
    def verificar_autenticacao(self) -> bool:
        """
        Verifica se o token ainda é válido usando validação local JWT
        
        Returns:
            True se autenticado e token válido
        """
        if not self.token or not self.autenticado:
            return False
        
        # Usa a mesma lógica de validação local que _validar_sessao
        try:
            partes = self.token.split(".")
            if len(partes) < 2:
                return False
            
            payload_b64 = partes[1]
            padding = "=" * (-len(payload_b64) % 4)
            payload_bytes = base64.urlsafe_b64decode(payload_b64 + padding)
            payload = json.loads(payload_bytes.decode("utf-8"))
            
            exp = payload.get("exp")
            if exp is None:
                return False
            
            agora = int(time.time())
            return agora < int(exp)
            
        except Exception:
            return False
    
    def desconectar(self):
        """
        Limpa dados de autenticação e fecha sessão para evitar vazamento de memória
        """
        # Limpa dados de autenticação
        self.token = None
        self.autenticado = False
        
        # Limpa cookies e headers da sessão
        if self.sessao:
            self.sessao.cookies.clear()
            self.sessao.headers.clear()
            
            # Fecha a sessão para liberar recursos
            try:
                self.sessao.close()
            except Exception:
                pass  # Ignora erros ao fechar sessão