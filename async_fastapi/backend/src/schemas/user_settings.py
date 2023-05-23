from enum import Enum

from pydantic import BaseModel

class StockMarkets(str, Enum):
    binance = 'Binance'
    bybit = 'Bybit'
    okx = 'OKX'


class UserSettingsModel(BaseModel):
    user_id: int
    stock_market: StockMarkets
    hashed_key: str
    hashed_secret: str
    update_date: int
    is_enable: int
    is_active: int


class UserSettingsCreate(BaseModel):
    user_id: int | None
    stock_market: StockMarkets
    hashed_key: str
    hashed_secret: str


class UserSettingsUpdate(UserSettingsModel):
    pass


class UserSettingsInfo(BaseModel):
    stock_market: StockMarkets
    hashed_key: str
    hashed_secret: str
