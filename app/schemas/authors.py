from pydantic import BaseModel

class BaseAuthor(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    photo: str
    group: str
    year_group: int
    class_group: int

class Author(BaseAuthor):
    id: int

class ActualAuthor(BaseModel):
    id: int
    name: str
    surname: str
    photo: str
    group: str
    year_group: int
    class_group: int
    work_image: str

