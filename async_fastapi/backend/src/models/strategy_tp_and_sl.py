from fastapi_users.models import ID
from sqlalchemy import Integer, Column, String, ForeignKeyConstraint, Float

from src.db.db import Base


class StrategyTpAndSl(Base):
    __tablename__ = "strategy_tp_and_sl"

    id: ID = Column(Integer, primary_key=True)
    strategy_id: int = Column(Integer, nullable=False, index=True)
    type: str = Column(String(length=15), nullable=False)
    lot_volume: float = Column(Float, default=1.0, nullable=False)
    price_by_margin: float = Column(Float, default=0.0, nullable=False)
    price_by_price: float = Column(Float, default=0.0, nullable=False)
    callback_rate: float = Column(Float, default=0.0, nullable=False)
    bind: int = Column(Integer, nullable=True)

    ForeignKeyConstraint(
        ('strategy_id',),
        ('user_trade_strategy.id',),
        use_alter=True,
        name="fk_strategy_tp_sl",
    )
