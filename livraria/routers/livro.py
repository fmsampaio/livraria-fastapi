from typing import List
from fastapi import APIRouter, Depends, Response, status, HTTPException
from ..database import SessionLocal, get_db
from .. import models, schemas

router = APIRouter(
    tags = ['Livros'],
    prefix = '/livros'
)

@router.get('/', response_model=List[schemas.LivroShow])
def list_all(db: SessionLocal = Depends(get_db)):
    livros = db.query(models.Livro).all()
    return livros

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.LivroShow)
def create(request: schemas.Livro, db: SessionLocal = Depends(get_db)):
    
    query_editora = db.query(models.Editora).filter(models.Editora.id == request.editora_id)
    if not query_editora.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'editora with id equals to {request.editora_id} was not found')
    
    query_categoria = db.query(models.Categoria).filter(models.Categoria.id == request.categoria_id)
    if not query_categoria.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'categoria with id equals to {request.categoria_id} was not found')
    
    new_livro = models.Livro(
        titulo = request.titulo,
        ISBN = request.ISBN,
        preco = request.preco,
        quantidade = request.quantidade,
        editora_id = request.editora_id,
        categoria_id = request.categoria_id
    )

    for autor_id in request.autores:
        autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
        if not autor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'autor with id equals to {autor_id} was not found')
        new_livro.autores.append(autor)

    db.add(new_livro)
    db.commit()
    db.refresh(new_livro)

    return new_livro

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.LivroShow)
def retrieve(id: int, db: SessionLocal = Depends(get_db)):
    livro = db.query(models.Livro).filter(models.Livro.id == id).first()
    if not livro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'livro with id equals to {id} was not found')
    return livro
