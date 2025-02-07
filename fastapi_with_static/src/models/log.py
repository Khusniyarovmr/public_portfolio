from sqlalchemy import Column, String, DateTime, CHAR, Index
from sqlalchemy.dialects.mysql import BIGINT

from src.db.postgres import Base


class Log(Base):
    __tablename__ = "log"

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    created = Column(DateTime(timezone=False), nullable=False)
    int_id = Column(CHAR(16), nullable=False)
    str_row = Column(String)
    address = Column(String)

    __table_args__ = (
        Index("log_address_idx", "address", postgresql_using="hash"),
    )
