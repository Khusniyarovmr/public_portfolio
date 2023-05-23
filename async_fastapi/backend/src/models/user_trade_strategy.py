from datetime import datetime

from fastapi_users.models import ID
from sqlalchemy import Integer, Column, String, ForeignKeyConstraint, Float, DateTime

from src.db.db import Base


class UserTradeStrategy(Base):
    __tablename__ = "user_trade_strategy"
    id: ID = Column(Integer, primary_key=True)
    name: str = Column(String, nullable=True)
    user_id: int = Column(Integer, nullable=False, index=True)
    symbol_id: int = Column(Integer, nullable=False)
    signal_name: str = Column(String(length=50), nullable=False)
    type: str = Column(String(length=50), default='Standard', nullable=False)
    stock_market: str = Column(String(length=50), default='Binance', nullable=False)
    create_time: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    lot_quantity: float = Column(Float, default=0.0, nullable=False)
    lot_percent: float = Column(Float, default=0.0, nullable=False)
    leverage: int = Column(Integer, default=10, nullable=False)
    averaging: int = Column(Integer, default=1, nullable=False)
    averaging_count: int = Column(Integer, default=3, nullable=False)
    averaging_volume: int = Column(Integer, default=2, nullable=False)
    tp_enable: int = Column(Integer, default=1, nullable=False)
    sl_enable: int = Column(Integer, default=0, nullable=False)
    is_active: int = Column(Integer, default=1, nullable=False)
    ForeignKeyConstraint(
        ('user_id', 'symbol_id'),
        ('user.id', 'symbol.id'),
        use_alter=True,
        name="fk_user_trade_strategy",
    )
