from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from ..config.db import Base

from .author import Author as AuthorModel

class Work(Base):
    __tablename__ = 'work'

    id: Mapped[int] = mapped_column(primary_key=True,nullable=False)

    date: Mapped[str] = mapped_column(TIMESTAMP, nullable=False)

    title: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str] = mapped_column(String(500), nullable=False)
    
    image: Mapped[str] = mapped_column(String(50), nullable=False)

    author: Mapped[int] = mapped_column(ForeignKey(AuthorModel.id), nullable=False)
    
    

# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#simple-select
