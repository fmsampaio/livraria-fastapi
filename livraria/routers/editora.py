from fastapi import APIRouter

router = APIRouter(
    tags = ['Editora'],
    prefix = '/editoras'
)

@router.get('/')
def list_all():
    return 'listing all editoras...'