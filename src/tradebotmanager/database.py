from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Type
from env_variables import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

BancoDeDados = sessionmaker(autocommit=False, autoflush=False, bind=engine, pool_pre_ping=True)

ModelBase: Type = declarative_base()

def obter_sessao():
    sessao = BancoDeDados()
    try:
        yield sessao
    finally:
        sessao.close()