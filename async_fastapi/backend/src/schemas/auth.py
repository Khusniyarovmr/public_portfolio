from fastapi_users import schemas
from typing import Optional
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    email: EmailStr
    username: str
    telegram_chat_id: Optional[int]
    role_id: int
    first_name: Optional[str]
    last_name: Optional[str]


    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str = 'CoolTrader'
    email: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]



class TelegramUserCreate(UserCreate):
    telegram_chat_id: int

class UserUpdate(schemas.BaseUserUpdate):
    password: Optional[str]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    telegram_chat_id: Optional[int]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
