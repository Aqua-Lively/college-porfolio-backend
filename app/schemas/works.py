from pydantic import BaseModel
from datetime import date
from typing import List

class InfoWork(BaseModel):
    date:date
    title:str
    description:str
    image:str
    author:int
    types: List[int]

class BaseWork(BaseModel):
    date: date
    title: str
    description: str
    image: str
    author: int

class Work(BaseModel):
    work_id: int
    image: str
    type_id: List[int]
    icon: List[str]


