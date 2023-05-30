import csv
import os
import pathlib
import random
from typing import NamedTuple

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from models.location import Location as LocationModel
from models.truck import Truck as TruckModel


class Locations(NamedTuple):
    city: str
    state: str
    zip_code: str
    latitude: str
    longitude: str


async def insert_loc_from_file(db: AsyncSession) -> None:
    locations = _get_locations_from_csv()
    async with db.begin() as session:
        for obj in locations:
            stmt = insert(LocationModel).values(
                city=obj.city,
                state=obj.state,
                zip_code=obj.zip_code,
                latitude=obj.latitude,
                longitude=obj.longitude,
            )
            await session.execute(stmt)


def _get_locations_from_csv() -> list[Locations]:
    locations_data: list[Locations] = []
    p = pathlib.Path(__file__)
    filepath = os.path.join(p.parent.parent.parent.parent, 'uszips.csv')
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file, delimiter=',')
        for line in reader:
            loc = Locations(
                city=line['city'],
                state=line['state_name'],
                zip_code=line['zip_code'],
                latitude=line['lat'],
                longitude=line['lng']
            )
            locations_data.append(loc)
    return locations_data


async def insert_trucks_on_init(db: AsyncSession) -> None:
    async with db.begin() as session:
        location_count = await session.execute(select(func.max(LocationModel.id)))
        max_loc_count = location_count.scalar()
        for i in range(20):
            car_number = _get_rnd_car_number()
            stmt = insert(TruckModel).values(
                truck_number=car_number,
                location_id=_get_random(1, 1000),
                capacity=_get_random(1, max_loc_count),
                is_active=1,
            )
            await session.execute(stmt)


def _get_rnd_car_number() -> str:
    rnd_car_num = _get_random(1000, 9999)
    rnd_literal = chr(_get_random(97, 123))
    return str(rnd_car_num) + rnd_literal


def _get_random(a: int, b: int) -> int:
    return random.randint(a, b)
