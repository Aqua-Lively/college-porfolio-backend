from sqlalchemy import Column, Integer, String, ForeignKey
from ..config.db import Base
from .author import Author as AuthorModel
from .type import Type as TypeModel

class Work_Type(Base):
    __tablename__ = 'works_types'

    type_id = Column(Integer, ForeignKey(AuthorModel.id), nullable=False, primary_key=True)
    work_id = Column(Integer, ForeignKey(TypeModel.id), nullable=False, primary_key=True)
