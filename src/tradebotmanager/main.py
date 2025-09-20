from fastapi import FastAPI

app = FastAPI(
    title="TradeBotManager", 
    description="Sistema de Gerenciamento de Bots de Trading",
    version="0.1.0"
)

@app.head("/health")
async def obter_status():
    """Endpoint HEAD para verificar status da API - compatível com UptimeRobot free"""
    return {"status": "ativo", "versao": "0.1.0"}