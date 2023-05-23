from datetime import datetime

from fastapi_users.models import ID
from sqlalchemy import Column, Float, String, DateTime, BigInteger, Boolean

from src.db.db import Base


class BinanceOrder(Base):
    __tablename__ = 'binance_order'

    order_id: ID = Column(BigInteger, primary_key=True)
    symbol: str = Column(String(length=50), nullable=False)
    status: str = Column(String(length=50), nullable=False)
    client_order_id: str = Column(String(length=50), nullable=False)
    price: float = Column(Float, nullable=False)
    avg_price: float = Column(Float, nullable=False)
    orig_qty: float = Column(Float, nullable=False)
    executed_qty: float = Column(Float, nullable=False)
    cum_qty: float = Column(Float, nullable=False)
    cum_quote: float = Column(Float, nullable=False)
    time_in_force: str = Column(String(length=50), nullable=False)
    type: str = Column(String(length=50), nullable=False)
    reduce_only: bool = Column(Boolean, nullable=False)
    close_position: bool = Column(Boolean, nullable=False)
    side: str = Column(String(length=50), nullable=False)
    position_side: str = Column(String(length=50), nullable=False)
    stop_price: float = Column(Float, nullable=False)
    working_type: str = Column(String(length=50), nullable=False)
    price_protect: bool = Column(Boolean, nullable=False)
    orig_type: str = Column(String(length=50), nullable=False)
    update_time: int = Column(BigInteger, nullable=False)
    create_time: datetime = Column(DateTime, nullable=False, default=datetime.utcnow())
