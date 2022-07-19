from fastapi import APIRouter, Depends, Response, status, HTTPException

from livraria.routers import utils
from ..database import SessionLocal, get_db
from .. import models, schemas

router = APIRouter(
    tags = ['Categorias'],
    prefix = '/categorias'
)

@router.get('/')
def list_all(db: SessionLocal = Depends(get_db)):
    categorias = db.query(models.Categoria).all()
    return categorias

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Categoria, db: SessionLocal = Depends(get_db)):
    new_categoria = models.Categoria(descricao=request.descricao)
    db.add(new_categoria)
    db.commit()
    db.refresh(new_categoria)
    return new_categoria

@router.get('/{id}', status_code=status.HTTP_200_OK)
def retrieve(id: int, db: SessionLocal = Depends(get_db)):
    categoria = utils.checkCategoriaById(id, db).first()
    return categoria

@router.delete('/{id}')
def destroy(id: int, db: SessionLocal = Depends(get_db)):
    query = utils.checkCategoriaById(id, db)
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Categoria, db: SessionLocal = Depends(get_db)):
    query = utils.checkCategoriaById(id, db)
    query.update( request.dict(), synchronize_session=False )
    db.commit()
    return query.first()