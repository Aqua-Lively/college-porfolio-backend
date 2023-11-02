from sqlalchemy import Column, Integer, String

from ..config.db import Base

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(20), nullable=False)
    login = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(50),  nullable=False)
    photo = Column(String(50), nullable=False)
