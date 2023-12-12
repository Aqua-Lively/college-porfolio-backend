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

from ..schemas import Work, InfoWork, ActualWork


from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy import select, func
from sqlalchemy import String

from typing import List, Annotated, Union

router = APIRouter(
    prefix="/api/works",
    tags=['Works']
)

@router.get('/', response_description='List of all works', response_model=List[List[Work]], status_code=status.HTTP_200_OK)
def get_all_works(db: Session=Depends(get_db)):

    stmt = select(WorkModel)

    works = db.execute(stmt).fetchall()

    if works == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Nothing found'
        )
    
    return works


@router.get('/actual', response_description='List of all works', response_model=List[ActualWork], status_code=status.HTTP_200_OK)
def get_all_works(db: Session = Depends(get_db)):

    stmt = select(
        WorkModel.id.label('work_id'),
        WorkModel.image,
        func.array_agg(Work_TypeModel.type_id).label('type_id'),
        func.array_agg(TypeModel.icon.cast(String(20))).label('icon')
    ).join(
        Work_TypeModel, WorkModel.id == Work_TypeModel.work_id
    ).join(
        TypeModel, Work_TypeModel.type_id == TypeModel.id
    ).group_by(
        WorkModel.id, WorkModel.image
    )

    works = db.execute(stmt).fetchall()

    if works == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nothing found'
        )
    
    return works


@router.get('/actual/{page}&{count}', response_description='List of all works', response_model=List[ActualWork], status_code=status.HTTP_200_OK)
def get_all_works(page: int, count: int, db: Session = Depends(get_db)):
    
    stmt = select(
        WorkModel.id.label('work_id'),
        WorkModel.image,
        func.array_agg(Work_TypeModel.type_id).label('type_id'),
        func.array_agg(TypeModel.icon.cast(String(20))).label('icon')
    ).join(
        Work_TypeModel, WorkModel.id == Work_TypeModel.work_id
    ).join(
        TypeModel, Work_TypeModel.type_id == TypeModel.id
    ).group_by(
        WorkModel.id, WorkModel.image
    ).limit(count).offset(page*count-(count-1) if page!= 0 else 0)

    print(stmt)
    works = db.execute(stmt).fetchall()

    if works == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nothing found'
        )
    
    return works
    


@router.get('/actual/{page}&{count}/types', response_description='List of all works', response_model=List[ActualWork], status_code=status.HTTP_200_OK)
def get_all_works(page: int, count: int, types: Union[List[int], None] = None, db: Session = Depends(get_db)):
    

    # stmt_count = select(
    #     WorkModel.id.label('work_id'),
    #     WorkModel.image,
    #     func.array_agg(Work_TypeModel.type_id).label('type_id'),
    #     func.array_agg(TypeModel.icon.cast(String(20))).label('icon')
    # ).join(
    #     Work_TypeModel, WorkModel.id == Work_TypeModel.work_id
    # ).join(
    #     TypeModel, Work_TypeModel.type_id == TypeModel.id
    # ).where(
    #     Work_TypeModel.type_id.in_(types)
    # ).group_by(
    #     WorkModel.id, WorkModel.image
    # )




    # stmt_count = select(
    #     WorkModel.id.label('work_id'),
    #     WorkModel.image,
    #     func.array_agg(Work_TypeModel.type_id).label('type_id'),
    #     func.array_agg(TypeModel.icon.cast(String(20))).label('icon')
    # ).join(
    #     Work_TypeModel, WorkModel.id == Work_TypeModel.work_id
    # ).join(
    #     TypeModel, Work_TypeModel.type_id == TypeModel.id
    # ).where(
    #     Work_TypeModel.type_id.in_(types)
    # ).group_by(
    #     WorkModel.id, WorkModel.image
    # )


    query1 = db.query(func.count(WorkModel.id), WorkModel).limit(1)
    print('++++++++++++++++++++++++++++++++++++++++++++++++')
    print(query1)
    print('++++++++++++++++++++++++++++++++++++++++++++++++')
    print('================================================')
    results = query1.all()
    print(results)
    print('================================================')
    # print(stmt_count)
    # count_rows = db.execute(stmt_count.count()).scalar()

    # print(count_rows)








    from sqlalchemy import distinct






    stmt_table = select(
        WorkModel.id.label('work_id'),
        WorkModel.image,
        func.array_agg(Work_TypeModel.type_id).label('type_id'),
        func.array_agg(TypeModel.icon.cast(String(20))).label('icon')
    ).join(
        Work_TypeModel, WorkModel.id == Work_TypeModel.work_id
    ).join(
        TypeModel, Work_TypeModel.type_id == TypeModel.id
    ).where(
        Work_TypeModel.type_id.in_(types)
    ).group_by(
        WorkModel.id, WorkModel.image
    ).limit(count).offset(page*count-(count-1) if page!= 0 else 0)

    # count_rows = db.execute(stmt_count).fetchall()

    # print(count_rows)

    works = db.execute(stmt_table).fetchall()

    if works == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nothing found'
        )
    
    return works



@router.get('/id/{id}', response_description='Get work by id', response_model=Work, status_code=status.HTTP_200_OK)
def get_work_by_id(id: int, db: Session=Depends(get_db)):


    stmt = select(WorkModel).where(WorkModel.id == id).limit(1)
    work = db.execute(stmt).scalar()

    if work is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nothing found"
        )

    return work


@router.post('/', response_description='Create new work', response_model=Work, status_code=status.HTTP_201_CREATED)
def create_work(work: InfoWork, db: Session=Depends(get_db)):


    try:

        types = getattr(work, 'types')
        delattr(work, 'types')

        new_work = db.execute(
            insert(WorkModel).returning(WorkModel), 
            [{**work.model_dump()}]
        ).scalar()
        
        for type in types:
            db.execute(
                insert(Work_TypeModel).values(
                    work_id=new_work.id,
                    type_id=type
                )
            )

    except:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            default=f'Не удалось добавить новую работу'
        )
    
    else:
        db.commit()
        return new_work
    

from typing import Union

# @router.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[int, None] = None):
#     return {"item_id": item_id, "q": q}


from typing import Annotated
from fastapi import Path

@router.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results