from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .database import Base

class Editora(Base):
    __tablename__ = 'editoras'
    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String)
    site = Column(String)

    livros = relationship("Livro", back_populates="editora")

class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key = True, index = True)
    nome = Column(String)
    livros = relationship("Livro", secondary='livros_autores', back_populates='autores')

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key = True, index = True)
    descricao = Column(String)

    livros = relationship("Livro", back_populates="categoria")

class Livro(Base):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key = True, index = True)
    titulo = Column(String)
    ISBN = Column(String)
    preco = Column(Float)
    quantidade = Column(Integer)
    autores = relationship("Autor", secondary='livros_autores', back_populates='livros')
    
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="livros")
    
    editora_id = Column(Integer, ForeignKey("editoras.id"))
    editora = relationship("Editora", back_populates="livros")

livros_autores = Table(
    'livros_autores', Base.metadata,
    Column('livro_id', ForeignKey('livros.id'), primary_key=True),
    Column('autor_id', ForeignKey('autores.id'), primary_key=True)
)