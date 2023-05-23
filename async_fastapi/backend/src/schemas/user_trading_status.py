from pydantic import BaseModel
from sqlalchemy import DateTime


class UserTradingStatusModel(BaseModel):
    user_id: int
    status: bool
    update_time: DateTime


class UserTradingStatusCreate(UserTradingStatusModel):
    pass


class UserTradingStatusUpdate(UserTradingStatusModel):
    pass
