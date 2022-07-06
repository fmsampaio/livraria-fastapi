from fastapi import FastAPI
from .routers import editora, autor, categoria, livro
from .database import Base, engine

app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(editora.router)
app.include_router(autor.router)
app.include_router(categoria.router)
app.include_router(livro.router)
