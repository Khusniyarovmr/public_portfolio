from pydantic import BaseModel
from datetime import datetime


class PositionBase(BaseModel):
    user_id: int
    stock_market: str
    signal_name: str
    strategy_id: int
    create_time: datetime | None
    close_time: datetime | None
    symbol_id: int
    side: str | None
    lot: float
    first_order_lot: float | None
    open_price: float | None
    close_price: float | None
    point: str | None
    status: str
    count: int


class PositionModel(PositionBase):
    id: int


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionModel):
    pass
