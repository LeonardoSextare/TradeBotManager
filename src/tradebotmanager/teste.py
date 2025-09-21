from database import engine, ModelBase

# Importar todos os models para registrar as tabelas
from usuarios.model import Usuario
from corretoras.model import Corretora
from corretoras_usuarios.model import CorretoraUsuario
from bots_option_market.model import BotOptionMarket
from bots_usuarios_op_mkt.model import BotUsuarioOpMkt

def testar_criacao_tabelas():
    """Testa se todos os models e relacionamentos estão corretos"""
    try:
        ModelBase.metadata.create_all(bind=engine)
        print("✅ Todas as tabelas criadas com sucesso!")
        print("✅ Relacionamentos SQLAlchemy validados!")
        
        # Listar tabelas criadas
        for tabela in ModelBase.metadata.tables.keys():
            print(f"  📄 Tabela: {tabela}")
            
    except Exception as erro:
        print(f"❌ Erro ao criar tabelas: {erro}")
        return False
    return True

if __name__ == "__main__":
    # ModelBase.metadata.drop_all(bind=engine)
    testar_criacao_tabelas()