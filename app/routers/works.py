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

from ..schemas import BaseWork,Work 


from sqlalchemy.orm import Session

from typing import List

router = APIRouter(
    prefix="/api/works",
    tags=['Works']
)

@router.get('/', response_description='List of all works', response_model=List[Work], status_code=status.HTTP_200_OK)
def get_all_works(db: Session=Depends(get_db)):
    works = db.query(WorkModel).all()

    if works == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Nothing found'
        )
    
    return works

@router.post('/', response_description='Create new work', response_model=Work, status_code=status.HTTP_201_CREATED)
def create_work(work: BaseWork, db: Session=Depends(get_db)):
    # new_work = WorkModel(**work.model_dump())
    new_work = WorkModel(
        title=work.title,
        description=work.description,
        date=work.date,
        image=work.image,
        author=work.author
    )
    print('===========================')
    print(work)
    print('===========================')
    db.add(new_work) 

    db.flush()


    db.commit()

    return new_work