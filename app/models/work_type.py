from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..config.db import Base
# from .author import Author as AuthorModel
from .work import Work as WorkModel
from .type import Type as TypeModel

class Work_Type(Base):
    __tablename__ = 'work_type'

    work_id: Mapped[int] = mapped_column(ForeignKey(WorkModel.id), nullable=False, primary_key=True)
    
    type_id: Mapped[int] = mapped_column(ForeignKey(TypeModel.id), nullable=False, primary_key=True)