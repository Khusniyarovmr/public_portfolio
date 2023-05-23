from pydantic import BaseModel
from datetime import datetime


class SymbolBase(BaseModel):
    stock_market: str
    symbol: str
    pair: str
    status: str | None
    pricePrecision: int
    quantityPrecision: int


class SymbolModel(SymbolBase):
    id: int
    update_date: datetime
    is_enable: int


class SymbolCreate(SymbolBase):
    update_date: datetime
    is_enable: int


class SymbolUpdate(SymbolModel):
    pass


class SymbolTradeInfo(BaseModel):
    pricePrecision: int
    quantityPrecision: int
