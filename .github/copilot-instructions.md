# TradeBotManager - Instruções para IA

## Sobre o Projeto
Sistema de gerenciamento de bots de trading para corretoras. Projeto pessoal para resolver problema real + aprendizado.

**Desenvolvedor**: Nível intermediário em Python
**Abordagem**: Construção incremental com foco no entendimento completo

## Stack Técnica Definida
- **Backend**: FastAPI
- **Banco**: Supabase (PostgreSQL)
- **ORM**: SQLAlchemy + Pydantic (abordagem tradicional)
- **Migrations**: Alembic
- **Deploy**: Render
- **Gerenciador de Pacotes**: UV
- **Linter**: Ruff (em aprendizado)

## Filosofia do Código
- **Idioma**: Código em português (variáveis, funções, comentários)
- **Legibilidade**: Sempre priorizar clareza sobre "cleverness"
- **Abordagem ORM**: SQLAlchemy + Pydantic separados (não SQLModel)
- **Fail Fast**: Programa deve quebrar rapidamente quando algo está errado
- **Exceções**: Nunca ignorar sem motivo válido; apenas suprimir em operações críticas
- **Incremental**: Cada feature desenvolvida passo a passo

## Papel da IA
**PARCEIRO SENIOR**, não code agent automático:
- Explicar conceitos e decisões técnicas
- Discutir problemas antes de implementar
- Ensinar padrões e melhores práticas
- Responder dúvidas detalhadamente
- Quando implementar: sempre explicar o que está sendo feito

## Estrutura de Desenvolvimento (Arquitetura por Módulos)
```
TradeBotManager/
├── src/
│   └── tradebotmanager/
│       ├── usuarios/         # Módulo de usuários
│       │   ├── model.py      # SQLAlchemy models
│       │   ├── repository.py # Acesso a dados
│       │   ├── service.py    # Lógica de negócio
│       │   ├── controller.py # Rotas FastAPI
│       │   └── schema.py     # Pydantic schemas
│       ├── bots/             # Módulo de bots
│       │   ├── model.py
│       │   ├── repository.py
│       │   ├── service.py
│       │   ├── controller.py
│       │   └── schema.py
│       ├── corretoras/       # Módulo de corretoras
│       │   └── ... (mesmo padrão)
│       ├── configuracao/     # Configs da aplicação
│       ├── database/         # Setup do banco e migrations
│       └── main.py           # Ponto de entrada FastAPI
├── alembic/                  # Migrations do banco
├── tests/                    # Testes (espelhando estrutura src/)
└── docs/                     # Documentação
```
```
Ainda não definido
```

## Convenções de Nomenclatura
```python
# Classes: PascalCase em português
class GerenciadorBot:
    pass

# Funções e variáveis: snake_case em português
def obter_posicoes_abertas():
    nome_corretora = "binance"
    return posicoes_ativas

# Constantes: UPPER_CASE em português
TEMPO_LIMITE_REQUISICAO = 30
```

## Padrões de Desenvolvimento

### Arquitetura por Módulos
Cada módulo (usuarios, bots, corretoras) segue o padrão:
```python
# model.py - Definição da tabela no banco
from sqlalchemy import Column, Integer, String
from database.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

# schema.py - Validação entrada/saída da API
from pydantic import BaseModel, EmailStr

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr

class UsuarioResponse(UsuarioSchema):
    id: int
    
    class Config:
        from_attributes = True

# repository.py - Acesso a dados
from sqlalchemy.orm import Session
from .model import Usuario

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def buscar_por_email(self, email: str) -> Usuario | None:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

# service.py - Lógica de negócio
from .repository import UsuarioRepository
from .schema import UsuarioSchema

class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository
    
    def criar_usuario(self, dados: UsuarioSchema) -> Usuario:
        if self.repository.buscar_por_email(dados.email):
            raise ValueError("Email já cadastrado")
        # ... lógica de criação

# controller.py - Rotas FastAPI
from fastapi import APIRouter, Depends
from .service import UsuarioService
from .schema import UsuarioSchema, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=UsuarioResponse)
async def criar_usuario(dados: UsuarioSchema, service: UsuarioService = Depends()):
    return service.criar_usuario(dados)
```

### Database e Migrations
```python
# database/base.py - Configuração base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Conexão com Supabase
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# alembic/env.py - Configuração do Alembic
# Alembic vai gerar migrations automaticamente baseado nos models
```

### Fail Fast
```python
# BOM: Falha imediata
def calcular_profit(preco_entrada: float, preco_saida: float) -> float:
    if preco_entrada <= 0 or preco_saida <= 0:
        raise ValueError("Preços devem ser positivos")
    return (preco_saida - preco_entrada) / preco_entrada

# RUIM: Continua com dados inválidos
def calcular_profit_ruim(preco_entrada, preco_saida):
    return (preco_saida - preco_entrada) / preco_entrada  # Pode dividir por zero
```

### Tratamento de Exceções
```python
# BOM: Tratamento específico
try:
    resposta_api = await requisitar_corretora()
except httpx.TimeoutError:
    logger.error("Timeout na requisição para corretora")
    raise ErroConexaoCorretora("Corretora não respondeu")
except httpx.HTTPStatusError as e:
    if e.response.status_code == 401:
        raise ErroAutenticacao("API key inválida")
    raise

# RUIM: Ignorar exceção sem motivo
try:
    fazer_algo_importante()
except Exception:
    pass  # Nunca fazer isso
```

## Ferramentas de Desenvolvimento

### UV (Gerenciador de Pacotes)
- Comandos básicos para aprender conforme necessário
- Setup inicial: `uv init`, `uv add`, `uv run`
- Dependências principais: `uv add fastapi sqlalchemy alembic psycopg2-binary`

### Ruff (Linter - Em Aprendizado)
- Configurar gradualmente
- Explicar regras quando aplicadas
- Ensinar como resolver warnings/erros

### Alembic (Migrations)
- **Nunca editar banco diretamente** - sempre via código
- Fluxo: Alterar model.py → `alembic revision --autogenerate` → `alembic upgrade head`
- Histórico versionado de mudanças no banco
- Rollback automático se necessário

## Abordagem de Implementação
1. **Discussão**: Sempre discutir o problema primeiro
2. **Design**: Pensar na estrutura antes de codificar
3. **Implementação**: Passo a passo com explicações
4. **Teste**: Validar cada componente
5. **Refatoração**: Melhorar após funcionar

## Áreas Indefinidas (A Definir Durante Desenvolvimento)
- Quais corretoras serão suportadas
- Interface de monitoramento

## Perguntas para Discussão
Quando trabalharmos juntos, sempre perguntar:
- "Por que escolher essa abordagem?"
- "Quais os trade-offs dessa decisão?"
- "Como isso afeta outras partes do sistema?"
- "Essa implementação está clara para revisão futura?"
