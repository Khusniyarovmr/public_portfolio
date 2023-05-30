from random import randint

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from src.models.location import Location as LocationModel
from src.models.truck import Truck as TruckModel
from src.schemas.truck import TruckCreate, TruckUpdate
from .base import RepositoryDB


class CRUDTruck(RepositoryDB[TruckModel, TruckCreate, TruckUpdate]):

    @staticmethod
    async def update_truck_location(db: AsyncSession) -> None:
        async with db.begin() as session:
            location_count = await session.execute(select(func.max(LocationModel.id)))
            location_count = location_count.scalar()
            for i in range(1, 21):
                rand_int = randint(0, location_count)
                stmt = update(TruckModel). \
                    values(location_id=rand_int). \
                    where(TruckModel.id == i)
                await session.execute(stmt)


truck_crud = CRUDTruck(TruckModel)

# if __name__ == '__main__':
#     asyncio.run(update_truck_location(async_session))
