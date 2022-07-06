from typing import List
from pydantic import BaseModel

class Editora(BaseModel):
    nome: str
    site: str

    class Config():
        orm_mode = True

class Autor(BaseModel):
    nome: str

    class Config():
        orm_mode = True

class Categoria(BaseModel):
    descricao: str

    class Config():
        orm_mode = True

class Livro(BaseModel):
    titulo: str
    ISBN: str
    quantidade: int
    preco: float
    editora_id: int
    categoria_id: int
    autores: List[int] = []
    
    class Config():
        orm_mode = True

class LivroShow(BaseModel):
    titulo: str
    ISBN: str
    quantidade: int
    preco: float
    editora: Editora
    autores: List[Autor] = []
    categoria: Categoria

    class Config():
        orm_mode = True

class EditoraShow(BaseModel):
    nome: str
    site: str
    livros: List[Livro] = []

    class Config():
        orm_mode = True