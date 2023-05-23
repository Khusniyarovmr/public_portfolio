from pydantic import BaseModel
from sqlalchemy import DateTime


class BlackListModel(BaseModel):
    user_id: int
    symbol_id: int
    create_date: DateTime
    update_date: DateTime
    is_enable: int


class BlackListCreate(BlackListModel):
    pass


class BlackListUpdate(BlackListModel):
    pass
