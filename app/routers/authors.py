from fastapi import(
    APIRouter,
    HTTPException,
    status,
    Depends
)

from ..config.db import get_db
from ..models import Author as AuthorModel
from ..models import Work as WorkModel
from ..models import Type as TypeModel
from ..models import Work_Type as Work_TypeModel

from ..schemas import BaseAuthor, Author


from sqlalchemy.orm import Session

from typing import List

router = APIRouter(
    prefix="/api/authors",
    tags=['Works']
)

@router.get('/', response_description='List of all Authors', response_model=List[Author], status_code=status.HTTP_200_OK)
def get_all_authors(db: Session=Depends(get_db)):

    authors = db.query(AuthorModel).all()

    if authors == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Nothing found'
        )
    
    return authors

@router.post('/', response_description='Create new author', response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(author: BaseAuthor, db: Session=Depends(get_db)):

    new_author = AuthorModel(**author.model_dump())

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author
