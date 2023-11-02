from pydantic import BaseModel

class BaseAuthor(BaseModel):
    name: str
    photo: str
    login: str
    password: str
    email: str


class Author(BaseAuthor):
    id: int