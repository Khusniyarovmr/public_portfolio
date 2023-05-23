from datetime import datetime

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users.models import ID
from sqlalchemy import Integer, Column, String, Boolean, ForeignKeyConstraint, DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import Base, get_session


class User(SQLAlchemyBaseUserTable[int], Base):
    id: ID = Column(Integer, primary_key=True)
    username: str = Column(String(length=300), nullable=True)
    first_name: str = Column(String(length=300), nullable=True)
    last_name: str = Column(String(length=400), nullable=True)
    role_id: int = Column(Integer, nullable=False, default=1)
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    telegram_chat_id: int = Column(Integer, unique=True, nullable=True)
    hashed_password: str = Column(String(length=1024), nullable=False)
    create_time: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    ForeignKeyConstraint(
        ('role_id',),
        ('role.id',),
        use_alter=True,
        name="fk_users",
    )


async def get_user_db(session: AsyncSession = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)
