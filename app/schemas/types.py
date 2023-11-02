from pydantic import BaseModel


class BaseType(BaseModel):
    type: str

class Type(BaseType):
    id: int