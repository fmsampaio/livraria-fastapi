from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status, HTTPException
from ..database import SessionLocal, get_db
from .. import models, schemas
from . import utils

router = APIRouter(
    tags = ['Livros'],
    prefix = '/livros'
)

@router.get('/', response_model=List[schemas.LivroShow])
def list_all(
    categoria: Optional[int] = -1, 
    editora: Optional[int] = -1,
    search: Optional[str] = "",
    maxpreco: Optional[float] = -1,
    db: SessionLocal = Depends(get_db)
    ):

    """
    livros_all = db.query(models.Livro).all()

    livros_return = []
    for livro in livros_all:
        livros_return.append(livro)
        if search != "" and not search in livro.titulo:
            livros_return = livros_return[:-1]
        if categoria != -1 and livro.categoria_id != categoria:
            livros_return = livros_return[:-1]
        if editora != -1 and livro.editora_id != editora:
            livros_return = livros_return[:-1]           
    """

    if search != "":
        livros = db.query(models.Livro).filter(models.Livro.titulo.contains(search)).all()
    elif categoria != -1:
        livros = db.query(models.Livro).filter(models.Livro.categoria_id == categoria).all()
    elif editora != -1:
        livros = db.query(models.Livro).filter(models.Livro.editora_id == editora).all()
    elif maxpreco != -1:
        livros = db.query(models.Livro).filter(models.Livro.preco <= maxpreco).all()
    else:
        livros = db.query(models.Livro).all()
    
    return livros

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.LivroShow)
def create(request: schemas.Livro, db: SessionLocal = Depends(get_db)):
    
    utils.checkEditoraById(request.editora_id, db)
    utils.checkCategoriaById(request.categoria_id, db)
    
    new_livro = models.Livro(
        titulo = request.titulo,
        ISBN = request.ISBN,
        preco = request.preco,
        quantidade = request.quantidade,
        editora_id = request.editora_id,
        categoria_id = request.categoria_id
    )

    for autor_id in request.autores:
        autor = utils.checkAutorById(autor_id, db).first()
        new_livro.autores.append(autor)

    db.add(new_livro)
    db.commit()
    db.refresh(new_livro)

    return new_livro

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.LivroShow)
def retrieve(id: int, db: SessionLocal = Depends(get_db)):
    livro = utils.checkLivroById(id, db).first()
    return livro

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.LivroShow)
def update(id: int, request: schemas.Livro, db: SessionLocal = Depends(get_db)):

    utils.checkCategoriaById(request.categoria_id, db)
    utils.checkEditoraById(request.editora_id, db)

    query = utils.checkLivroById(id, db)
    
    query.update( {
        'titulo' : request.titulo, 
        'ISBN' : request.ISBN,
        'quantidade' : request.quantidade,
        'preco': request.preco,
        'editora_id' : request.editora_id,
        'categoria_id' : request.categoria_id
    }, synchronize_session=False )
    
    livro = query.first()
    livro.autores = []

    for autor_id in request.autores:
        autor = utils.checkAutorById(autor_id, db).first()
        livro.autores.append(autor)

    db.commit()
    return query.first()

@router.delete('/{id}')
def destroy(id: int, db: SessionLocal = Depends(get_db)):
    query = utils.checkLivroById(id, db)
    
    query.first().autores = []

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)