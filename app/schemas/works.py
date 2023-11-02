from pydantic import BaseModel
from datetime import date
from typing import List

class BaseWork(BaseModel):
    date: date
    title: str
    description: str
    image: str
    author: int

class Work(BaseWork):
    id: int

class WorkWithType(BaseModel):
    date: date
    title: str
    description: str
    image: str
    author: int
    type: List[str]
