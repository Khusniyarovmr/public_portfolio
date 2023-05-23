from pydantic import BaseModel

class RedisMessage(BaseModel):
    type: str
    patter: str | None
    channel: bytes
    data: bytes
