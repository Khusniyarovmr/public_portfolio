from pydantic import BaseModel, Field


class StrategyModel(BaseModel):
    lot_quantity: float = Field(default=0.0)
    lot_percent: float = Field(default=0.0)
    leverage: int = Field(default=10)
    tp_margin: float = Field(default=0.2)
    tp_price: float = Field(default=0.02)
    tp_count: int = Field(default=3)
    tp_enable: int = Field(default=1)
    sl_margin: float = Field(default=0.2)
    sl_price: float = Field(default=0.02)
    sl_enable: int = Field(default=0)


class StrategyCreate(StrategyModel):
    pass


class StrategyUpdate(StrategyModel):
    pass
