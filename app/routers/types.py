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

from ..schemas import BaseType, Type


from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from typing import List

router = APIRouter(
    prefix="/api/types",
    tags=['Types']
)

@router.get('/', response_description='List of all types', response_model=List[List[Type]], status_code=status.HTTP_200_OK)
def get_all_types(db: Session=Depends(get_db)):

    stmt = select(TypeModel)

    types = db.execute(stmt).fetchall()

    if types == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Nothing found'
        )
    
    return types

@router.post('/', response_description='Create new types', response_model=Type, status_code=status.HTTP_201_CREATED)
def create_type(type: BaseType, db: Session=Depends(get_db)):

    try:
        new_type = db.execute(
            insert(TypeModel).returning(TypeModel),
            [{**type.model_dump()}]
        ).scalar()
    
    except:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            default=f'Не удалось добавить новый тип'
        )
    
    else:
        db.commit()
        return new_type

