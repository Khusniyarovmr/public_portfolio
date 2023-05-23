from fastapi_users.models import ID
from sqlalchemy import Integer, Column, String, JSON

from src.db.db import Base


class Role(Base):
    __tablename__ = "role"

    id: ID = Column(Integer, primary_key=True)
    name: str = Column(String(length=500), nullable=False)
    permission: JSON = Column(JSON, nullable=True)
    is_enable: int = Column(Integer, default=1, nullable=False)
