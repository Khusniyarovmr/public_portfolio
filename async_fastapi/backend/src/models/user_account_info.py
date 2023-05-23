from datetime import datetime

from fastapi_users.models import ID
from sqlalchemy import Integer, Column, Float, String, ForeignKeyConstraint, DateTime

from src.db.db import Base


class UserAccountInfo(Base):
    __tablename__ = "user_account_info"

    id: ID = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, nullable=False)
    stock_market: str = Column(String(length=50), nullable=False)
    type: str = Column(String, nullable=True)
    balance: float = Column(Float, default=0.0, nullable=False)
    last_update_date: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    ForeignKeyConstraint(
        ('user_id',),
        ('user.id',),
        use_alter=True,
        name="fk_user_account_info",
    )
