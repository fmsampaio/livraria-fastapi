from fastapi import FastAPI
from .routers import editora

app = FastAPI()

app.include_router(editora.router)
