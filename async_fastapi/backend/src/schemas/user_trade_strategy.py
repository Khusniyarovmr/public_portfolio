from datetime import datetime
from enum import Enum

from pydantic import BaseModel, validator


class TypeEnum(str, Enum):
    type_1 = 'Custom'
    type_2 = 'Through'


class StockMarketEnum(str, Enum):
    binance = 'Binance'
    bybit = 'Bybit'
    okx = 'OKX'


class UserTradeStrategyBase(BaseModel):
    name: str
    user_id: int
    symbol_id: int
    signal_name: str
    type: str
    stock_market: str
    lot_quantity: float
    lot_percent: float
    leverage: int
    averaging: int
    averaging_count: int
    averaging_volume: int
    tp_enable: int
    sl_enable: int
    is_active: int

    @validator('stock_market')
    def market_can_be(cls, v):  # noqa
        if v not in ['Binance', 'Bybit', 'OKX']:
            raise ValueError('Bad market name')
        return v.title()

    @validator('type')
    def type_can_be(cls, v):  # noqa
        if v not in ['Custom', 'Through']:
            raise ValueError('Bad strategy type')
        return v.title()

    class Config:
        allow_reuse = True


class UserTradeStrategyModel(UserTradeStrategyBase):
    id: int
    create_time: datetime

    class Config:
        orm_mode = True


class UserTradeStrategyCreate(UserTradeStrategyBase):
    pass

    class Config:
        orm_mode = True


class UserTradeStrategyUpdate(UserTradeStrategyModel):
    pass

    class Config:
        orm_mode = True


class UserTradeStrategyWithSymbol(UserTradeStrategyBase):
    id: int
    symbol: str | None

    class Config:
        orm_mode = True
