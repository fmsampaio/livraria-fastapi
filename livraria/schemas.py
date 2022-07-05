from pydantic import BaseModel

class Editora(BaseModel):
    nome: str
    site: str
