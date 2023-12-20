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

from ..schemas import BaseAuthor, Author, ActualAuthor


from sqlalchemy.orm import Session
from sqlalchemy import select, insert,func, String



from typing import List

router = APIRouter(
    prefix="/api/authors",
    tags=['Authors']
)


@router.get('/', response_description='List of all Authors', response_model=List[List[Author]], status_code=status.HTTP_200_OK)
def get_all_authors(db: Session=Depends(get_db)):

    stmt = select(AuthorModel)

    authors = db.execute(stmt).fetchall()

    if authors == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nothing found'  
        )
        
    return authors


@router.get('/actual/', response_description='List of all Authors', response_model=List[ActualAuthor], status_code=status.HTTP_200_OK)
def get_all_authors(db: Session=Depends(get_db)):

    stmt = select(
        AuthorModel.id,
        AuthorModel.name,
        AuthorModel.surname,
        AuthorModel.photo,
        AuthorModel.group,
        AuthorModel.year_group,
        AuthorModel.class_group,
        func.max(WorkModel.image).label('work_image')
    ).join(
        WorkModel, AuthorModel.id == WorkModel.author
    ).group_by(
        AuthorModel.id
    )

    authors = db.execute(stmt).fetchall()

    if authors == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nothing found'  
        )
    print(authors)
    return authors


@router.get('/actual/id/{id}', response_description='Get author by id', status_code=status.HTTP_200_OK)
def get_author_by_id(id: int, db: Session=Depends(get_db)):

    

    subquery = db.query(
        WorkModel.id,
        WorkModel.image,
        func.array_agg(Work_TypeModel.type_id).label('type_id'),
        func.array_agg(TypeModel.icon.cast(String(20))).label('icon'),
        WorkModel.author
    ).join(Work_TypeModel, WorkModel.id == Work_TypeModel.work_id).join(TypeModel, Work_TypeModel.type_id == TypeModel.id).group_by(WorkModel.id).subquery()

    result = db.query(
        AuthorModel.id,
        AuthorModel.name,
        AuthorModel.surname,
        AuthorModel.email,
        AuthorModel.photo,
        AuthorModel.group,
        AuthorModel.class_group,
        AuthorModel.year_group,
        func.array_agg(subquery.c.id).label('array_works_id'),
        func.array_agg(subquery.c.image).label('array_images'),
        func.array_agg(subquery.c.type_id).label('array_types'),
        func.array_agg(subquery.c.icon).label('array_icons')
    ).join(subquery, AuthorModel.id == subquery.c.author).filter(AuthorModel.id == 2).group_by(AuthorModel.id).all()

    result =  dict(result[0]._asdict())
    
    return result




@router.get('/id/{id}', response_description='Get author by id', response_model=Author, status_code=status.HTTP_200_OK)
def get_author_by_id(id: int, db: Session=Depends(get_db)):

    stmt = select(AuthorModel).where(AuthorModel.id == id).limit(1)
    author = db.execute(stmt).scalar()

    if author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Nothing found'
        )
    
    return author




@router.post('/', response_description='Create new author', response_model=Author, status_code=status.HTTP_201_CREATED)
def create_author(author: BaseAuthor, db: Session=Depends(get_db)):

    new_author = AuthorModel(**author.model_dump())

    db.add(new_author)
    db.commit()
    db.refresh(new_author)

    return new_author
