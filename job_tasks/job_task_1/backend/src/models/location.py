from sqlalchemy import Integer, Column, String

from db.db import Base


class Location(Base):
    __tablename__ = "location"
    id: int = Column(Integer, nullable=False, primary_key=True)
    city: str = Column(String(length=50), nullable=False)
    state: str = Column(String(length=100), nullable=False)
    zip_code: str = Column(String(length=50), nullable=False)
    latitude: str = Column(String(length=10))
    longitude: str = Column(String(length=10))
