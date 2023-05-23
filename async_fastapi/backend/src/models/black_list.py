from datetime import datetime

from fastapi_users.models import ID
from sqlalchemy import Integer, Column, DateTime, ForeignKeyConstraint

from src.db.db import Base


class BlackList(Base):
    __tablename__ = "black_list"
    id: ID = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, nullable=False)
    symbol_id: int = Column(Integer, nullable=False)
    create_date: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    update_date: DateTime = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    is_enable: int = Column(Integer, nullable=False)
    ForeignKeyConstraint(
        ('user_id', 'symbol_id'),
        ('user.id', 'symbol.id'),
        use_alter=True,
        name="fk_black_list",
    )
