# filepath: c:\Projects\TradeBotManager\test_model.py
from tradebotmanager.database import engine, ModelBase
from usuarios.model import Usuario  # Importa o modelo para registrar a tabela
from corretoras.model import Corretora  # Importa o modelo para registrar a tabela


ModelBase.metadata.create_all(bind=engine)
print("Tabela 'usuarios' criada com sucesso!")
print("Tabela 'corretoras' criada com sucesso!")
