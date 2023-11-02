from sqlalchemy import Column, Integer, String

from ..config.db import Base

class Type(Base):
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True, nullable=False)
    type = Column(String, nullable=False)
