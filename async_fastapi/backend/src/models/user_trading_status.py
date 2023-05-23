from datetime import datetime

from sqlalchemy import Integer, Column, DateTime, Boolean, ForeignKeyConstraint

from src.db.db import Base


class UserTradingStatus(Base):
    __tablename__ = "user_trading_status"
    user_id: int = Column(Integer, nullable=False, primary_key=True)
    status: bool = Column(Boolean, nullable=False, default=False)
    update_time: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    ForeignKeyConstraint(
        ('user_id',),
        ('user.id',),
        use_alter=True,
        name="fk_user_trading_status",
    )
