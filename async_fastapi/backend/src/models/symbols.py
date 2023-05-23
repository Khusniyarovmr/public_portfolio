from datetime import datetime

from fastapi_users.models import ID
from sqlalchemy import Integer, Column, String, DateTime, Index

from src.db.db import Base


class Symbol(Base):
    __tablename__ = "symbol"
    id: ID = Column(Integer, primary_key=True)
    stock_market: str = Column(String(length=30), nullable=True)
    update_date: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    is_enable: int = Column(Integer, nullable=False, default=1)
    symbol: str = Column(String(length=30), nullable=True)
    pair: str = Column(String(length=30), nullable=True)
    status: str = Column(String(length=30), nullable=True)
    price_precision: int = Column(Integer, nullable=True)
    quantity_precision: int = Column(Integer, nullable=True)

    __table_args__ = (
        Index('symbolindex', stock_market, symbol, unique=True),
    )
