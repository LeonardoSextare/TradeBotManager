from sqlalchemy import Column, Integer, String, Boolean
from database import ModelBase


class Corretora(ModelBase):
    __tablename__ = "corretoras"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    ativa = Column(Boolean, default=True, nullable=False)
