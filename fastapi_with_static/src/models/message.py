from sqlalchemy import Column, String, DateTime, Boolean, CHAR, Index

from src.db.postgres import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(String, primary_key=True)
    created = Column(DateTime(timezone=False), nullable=False)
    int_id = Column(CHAR(16), nullable=False)
    str_row = Column(String, nullable=False)
    status = Column(Boolean)

    __table_args__ = (
        Index("message_created_idx", "created"),
        Index("message_int_id_idx", "int_id"),
    )
