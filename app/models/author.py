from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ..config.db import Base

from typing import List


class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)

    name: Mapped[int] = mapped_column(String(20), nullable=False)

    surname: Mapped[str] = mapped_column(String(20), nullable=False)
    
    email: Mapped[str] = mapped_column(String(20), nullable=False)

    password: Mapped[str] = mapped_column(String(20), nullable=False)

    photo: Mapped[str] = mapped_column(String(200), nullable=False)

    group: Mapped[str] = mapped_column(String(20), nullable=False)

    year_group: Mapped[int] = mapped_column(Integer, nullable=False)

    class_group: Mapped[int] = mapped_column(Integer, nullable=False)

