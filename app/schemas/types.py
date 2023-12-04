from pydantic import BaseModel


class BaseType(BaseModel):
    type: str
    icon: str

class Type(BaseType):
    id: int