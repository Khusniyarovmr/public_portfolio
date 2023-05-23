from fastapi_users.models import ID
from sqlalchemy import Integer, Column, Float

from src.db.db import Base


class Strategy(Base):
    __tablename__ = "strategy"
    id: ID = Column(Integer, primary_key=True)
    lot_quantity: float = Column(Float, default=0.0, nullable=False)
    lot_percent: float = Column(Float, default=0.0, nullable=False)
    leverage: int = Column(Integer, default=10, nullable=False)
    tp_margin: float = Column(Float, default=0.2, nullable=False)
    tp_price: float = Column(Float, default=0.02, nullable=False)
    tp_count: int = Column(Integer, default=3, nullable=False)
    tp_enable: int = Column(Integer, default=1, nullable=False)
    sl_margin: float = Column(Float, default=0.2, nullable=False)
    sl_price: float = Column(Float, default=0.02, nullable=False)
    sl_enable: int = Column(Integer, default=0, nullable=False)
