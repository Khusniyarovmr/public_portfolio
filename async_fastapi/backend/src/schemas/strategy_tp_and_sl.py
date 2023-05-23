from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TypeVariants(str, Enum):
    var_1 = 'trailing_stop'
    var_2 = 'stop_loss'
    var_3 = 'take_profit'


class StrategyTPAndSLBase(BaseModel):
    strategy_id: int
    type: TypeVariants
    lot_volume: float
    price_by_margin: float
    price_by_price: float
    callback_rate: float
    bind: int


class StrategyTPAndSLModel(StrategyTPAndSLBase):
    id: int

    class Config:
        orm_mode = True


class StrategyTPAndSLCreate(StrategyTPAndSLBase):
    pass

    class Config:
        orm_mode = True


class StrategyTPAndSLUpdate(StrategyTPAndSLBase):
    id: Optional[int]

    class Config:
        orm_mode = True
