from pydantic import BaseModel, validator
from src.core.constants import Aliases


class SignalBase(BaseModel):
    name: str
    symbol: str
    type: str
    action: str
    lot: float
    price: float
    point: str | None

    @validator('action')
    def action_can_be(cls, v):
        if v.upper() in [Aliases.CLOSE,
                 Aliases.FLAT,
                 Aliases.EXIT,
                 Aliases.BUY,
                 Aliases.SELL]:
            return v.title()
        else:
            raise ValueError('Bad action in signal')

    class Config:
        orm_mode = True


class SignalModel(SignalBase):
    id: int

    class Config:
        orm_mode = True


class SignalsCreate(SignalBase):
    pass


class SignalsUpdate(SignalModel):
    pass


class SignalStatus(BaseModel):
    type: str
    action: str
    point: str | None
