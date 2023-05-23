from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BinanceOrderBase(BaseModel):
    user_id: int
    stock_market: str
    signal_id: int
    strategy_id: int
    create_time: Optional[datetime]
    close_time: Optional[datetime]
    symbol_id: int
    side: str
    type: str
    lot: float
    open_price: float
    close_price: float
    point: str
    status: str
    count: int
    market_order_id: int
    market_order_id_str: str


class BinanceOrderModel(BinanceOrderBase):
    id: int


class BinanceOrderCreate(BinanceOrderBase):
    pass


class BinanceOrderUpdate(BinanceOrderModel):
    pass
