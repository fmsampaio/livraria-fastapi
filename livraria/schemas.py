from typing import List
from pydantic import BaseModel

class Editora(BaseModel):
    nome: str
    site: str

class Autor(BaseModel):
    nome: str

class Categoria(BaseModel):
    descricao: str

class EditoraShow(BaseModel):
    id: int
    nome: str
    site: str

    class Config():
        orm_mode = True

class AutorShow(BaseModel):
    id: int
    nome: str

    class Config():
        orm_mode = True


class CategoriaShow(BaseModel):
    id: int
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
    
class LivroShow(BaseModel):
    id: int
    titulo: str
    ISBN: str
    quantidade: int
    preco: float
    editora: EditoraShow
    categoria: CategoriaShow
    autores: List[AutorShow] = []

    class Config():
        orm_mode = True
