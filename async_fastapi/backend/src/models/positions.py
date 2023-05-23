from datetime import datetime

from fastapi_users.models import ID
from sqlalchemy import Integer, Column, Float, String, DateTime, ForeignKeyConstraint, BigInteger, Index

from src.db.db import Base


class Position(Base):
    __tablename__ = 'position'

    id: ID = Column(BigInteger, primary_key=True)
    user_id: int = Column(Integer, index=True, nullable=False)
    stock_market: str = Column(String(length=50), nullable=False)
    signal_name: str = Column(String(length=100), nullable=False)
    strategy_id: int = Column(Integer, nullable=False)
    create_time: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    close_time: DateTime = Column(DateTime(timezone=True), nullable=True)
    symbol_id: int = Column(Integer, nullable=False)
    side: str = Column(String, nullable=False)
    lot: float = Column(Float, nullable=False)
    first_order_lot: float = Column(Float, nullable=False)
    open_price: float = Column(Float, nullable=False)
    close_price: float = Column(Float, nullable=True)
    point: str = Column(String(length=50), nullable=False)
    status: str = Column(String(length=50), nullable=False)
    count: int = Column(Integer, nullable=False, default=1)
    ForeignKeyConstraint(
        ('user_id', 'signal_id', 'symbol_id', 'strategy_id'),
        ('user.id', 'signal.id', 'symbol.id', 'user_trade_strategy.id'),
        use_alter=True,
        name="fk_position",
    )
    __table_args__ = (
        Index('posindex', user_id, strategy_id, symbol_id, signal_name, stock_market, unique=True),
    )
