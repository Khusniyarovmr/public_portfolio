from sqlalchemy import Integer, Column, String, ForeignKeyConstraint

from db.db import Base


class Truck(Base):
    __tablename__ = "truck"
    id: int = Column(Integer, nullable=False, primary_key=True)
    truck_number: str = Column(String, nullable=False, unique=True)
    location_id: int = Column(Integer, nullable=False)
    capacity: int = Column(Integer, nullable=False, default=0)
    is_active: int = Column(Integer, default=1, nullable=False)
    ForeignKeyConstraint(
        ('location_id',),
        ('location.id',),
        use_alter=True,
        name="fk_track_location",
    )
