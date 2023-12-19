from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..config.db import Base

class Type(Base):
    __tablename__ = 'type'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    icon: Mapped[str] = mapped_column(String(200), nullable=False)

