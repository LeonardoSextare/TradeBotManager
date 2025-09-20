from fastapi import FastAPI

app = FastAPI(
    title="TradeBotManager", 
    description="Sistema de Gerenciamento de Bots de Trading",
    version="0.1.0"
)

@app.head("/health")
async def obter_status():
    return {"status": "ativo", "versao": "0.1.0"}


if __name__ == "__main__":
    import uvicorn
    # Simples e direto
    uvicorn.run(app, host="0.0.0.0", port=8001)