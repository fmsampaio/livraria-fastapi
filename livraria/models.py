from sqlalchemy import Column, Integer, String
from .database import Base

class Editora(Base):
    __tablename__ = 'editoras'
    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String)
    site = Column(String)

class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String)

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key = True, index = True)
    descricao = Column(String)