from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    id: str
    created: datetime
    int_id: str
    str_row: str
    status: bool


class MessageCreate(Message):
    pass


class MessageUpdate(Message):
    pass
