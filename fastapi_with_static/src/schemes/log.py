from datetime import datetime

from pydantic import BaseModel


class Log(BaseModel):
    created: datetime
    int_id: str
    str_row: str
    address: str | None = None


class LogModel(Log):
    id: int


class LogCreate(Log):
    pass


class LogUpdate(Log):
    pass
