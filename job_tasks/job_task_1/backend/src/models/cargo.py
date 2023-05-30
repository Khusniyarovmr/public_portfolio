from datetime import datetime

from sqlalchemy import Integer, Column, String, ForeignKeyConstraint, DateTime

from src.db.db import Base


class Cargo(Base):
    __tablename__ = "cargo"
    id: int = Column(Integer, primary_key=True)
    pick_up_location: str = Column(String(length=10), nullable=False)
    delivery_location: str = Column(String(length=10), nullable=False)
    weight: int = Column(Integer, nullable=False)
    description: str = Column(String, nullable=True)
    create_Date: datetime = Column(DateTime, default=datetime.utcnow(), nullable=False)

    ForeignKeyConstraint(
        ('pick_up_location', 'delivery_location'),
        ('location.id', 'location.id'),
        use_alter=True,
        name="fk_cargo_location",
    )
