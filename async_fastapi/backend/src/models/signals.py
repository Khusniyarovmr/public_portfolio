from datetime import datetime

from fastapi_users.models import ID
from sqlalchemy import Integer, Column, Float, String, ForeignKeyConstraint, DateTime

from src.db.db import Base


class Signal(Base):
    __tablename__ = "signal"
    id: ID = Column(Integer, primary_key=True)
    name: str = Column(String(length=50), nullable=False)
    create_time: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    symbol: str = Column(String, nullable=False)
    type: str = Column(String(length=50), nullable=False)
    action: str = Column(String(length=50), nullable=False)
    lot: float = Column(Float, default=0.0, nullable=False)
    price: float = Column(Float, default=0.0, nullable=False)
    point: str = Column(String(length=50), nullable=False)
    ForeignKeyConstraint(
        ('symbol_id',),
        ('symbol.id',),
        use_alter=True,
        name="fk_signals",
    )
