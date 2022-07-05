from pydantic import BaseModel

class Editora(BaseModel):
    nome: str
    site: str

class Autor(BaseModel):
    nome: str

class Categoria(BaseModel):
    descricao: str