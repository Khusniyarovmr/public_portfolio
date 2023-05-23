from typing import Optional

from pydantic import EmailStr
from sqlalchemy.future import select

from src.core.security import get_password_hash
from src.db.db import async_session
from src.models.user import User
from src.schemas.auth import TelegramUserCreate


async def get_user_by_chat_id(chat_id: int) -> Optional[str]:
    query = select(User.username).where(User.telegram_chat_id == chat_id)
    async with async_session.begin() as session:
        user_info = await session.execute(query)
    return user_info.scalar_one_or_none()


async def registration_from_telegram(chat_id: int, username: str, email: EmailStr, pwd: str) -> User:
    hashed_password = get_password_hash(pwd)
    new_user = TelegramUserCreate(
        username=username,
        email=email,
        password=hashed_password,
        telegram_chat_id=chat_id
    )
    new_user_dict = new_user.dict()
    del new_user_dict['password']
    new_user_dict['hashed_password'] = hashed_password
    user_obj = User(**new_user_dict)
    async with async_session.begin() as session:
        session.add(user_obj)
        await session.commit()
    return user_obj
