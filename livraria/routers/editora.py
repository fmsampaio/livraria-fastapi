from fastapi import APIRouter, Depends
from ..database import SessionLocal, get_db
from .. import models, schemas

router = APIRouter(
    tags = ['Editora'],
    prefix = '/editoras'
)

@router.get('/')
def list_all(db: SessionLocal = Depends(get_db)):
    editoras = db.query(models.Editora).all()
    return editoras

@router.post('/')
def create(request: schemas.Editora, db: SessionLocal = Depends(get_db)):
    new_editora = models.Editora(nome=request.nome, site=request.site)
    db.add(new_editora)
    db.commit()
    db.refresh(new_editora)
    return new_editora
