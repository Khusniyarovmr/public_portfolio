from datetime import datetime

from sqlalchemy import Integer, Column, String, ForeignKeyConstraint, DateTime
from fastapi_users.models import ID
from src.db.db import Base


class UserSettings(Base):
    __tablename__ = "user_settings"
    id: ID = Column(Integer, nullable=False, primary_key=True)
    user_id: int = Column(Integer, nullable=False, unique=False)
    stock_market: str = Column(String(length=50), nullable=False)
    hashed_key: str = Column(String(length=1024), nullable=False)
    hashed_secret: str = Column(String(length=1024), nullable=False)
    update_date: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    is_enable: int = Column(Integer, default=1, nullable=False)
    is_active: int = Column(Integer, default=1, nullable=False)
    ForeignKeyConstraint(
        ('user_id',),
        ('user.id',),
        use_alter=True,
        name="fk_user_settings",
    )
