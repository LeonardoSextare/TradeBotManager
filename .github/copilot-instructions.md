# TradeBotManager - Instruções para IA

## Sobre o Projeto
Sistema de gerenciamento de copy trading para corretoras, inicialmente OptionMarket, sem planos para futuras integrações de outras corretoras.
 Projeto pessoal para resolver problema real + aprendizado.

**Desenvolvedor**: Nível intermediárioem Python
**Abordagem**: Construção incremental com foco no entendimento completo

## Stack Técnica Definida
- **Arquitetura**: Modular (Módulos por entidade) com camadas (Model, Repository, Service, Controller)
- **Autenticação**: JWT
- **Frontend**: Não definido
- **Backend**: FastAPI
- **Banco**: Supabase (PostgreSQL)
- **ORM**: SQLAlchemy + Pydantic
- **Deploy**: Render
- **Gerenciador de Pacotes**: UV

## Decisões de Projeto
- **Soft delete**: Usar campo booleano `ativo` para marcar registros como inativos
- **Simplicidade**: Evitar complexidade desnecessária
- **Somente o necessário**: Implementar apenas o que é essencial para a funcionalidade atual
- **Documentação**: Código autoexplicativo + docstrings claras e simples.

## Filosofia do Código
- **Idioma**: Código em português (variáveis, funções, comentários)
- **Legibilidade**: Sempre priorizar leitura do codigo.
- **Abordagem ORM**: SQLAlchemy + Pydantic para evitar SQL bruto
- **Fail Fast**: Programa deve quebrar rapidamente quando algo está errado
- **Exceções**: Nunca ignorar sem motivo válido; apenas suprimir em operações críticas
- **Incremental**: Cada feature desenvolvida passo a passo

## Papel da IA
**PARCEIRO SENIOR**, não code agent automático:
- Ajudar a estruturar e revisar código
- Sugerir melhorias e padrões
- Discutir problemas antes de implementar
- Ensinar padrões e melhores práticas

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
│       └── main.py           # Ponto de entrada
```
