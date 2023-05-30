from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.cargo import Cargo as CargoModel
from models.location import Location
from models.truck import Truck
from schemas.cargo import (
    CargoCreate,
    CargoUpdate,
    CargoModelWithAllTrucks,
    ListOfTrucks,
    CargoWithTruckCountBase
)
from services.crud.base import RepositoryDB
from services.get_distance_between_locations import get_distance
from services.logger.logger import logger


class CRUDCargo(RepositoryDB[CargoModel, CargoCreate, CargoUpdate]):
    # - Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
    async def get_cargo_with_trucks(self,
                                    db: AsyncSession,
                                    *,
                                    obj_in: int,
                                    cargo_info: tuple) -> CargoModelWithAllTrucks:
        stmt = select(Truck.id, Location.latitude, Location.longitude)
        stmt = stmt.join(Location, Location.id == Truck.location_id)  # noqa
        truck_list_cursor = await db.execute(stmt)
        truck_list = truck_list_cursor.fetchall()  # list[tuple[truck.id, truck.lat, truck.long]]

        truck_distance_info = []
        for truck, lat, long in truck_list:
            truck_info = (lat, long)
            distance = get_distance(cargo_info, truck_info)
            truck_distance_info.append(ListOfTrucks(truck_id=truck, distance=distance))

        cargo: CargoModel = await self.get(db, obj_in)

        cargo_obj = {
            'pick_up_location': cargo.pick_up_location,
            'delivery_location': cargo.delivery_location,
            'weight': cargo.weight,
            'description': cargo.description,
            'trucks': truck_distance_info
        }

        return CargoModelWithAllTrucks.parse_obj(cargo_obj)

    # - Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));
    @staticmethod
    async def get_all_cargo_with_distance(db: AsyncSession):
        stmt = select(Truck.id, Location.latitude, Location.longitude)
        stmt = stmt.join(Location, Location.id == Truck.location_id)  # noqa
        truck_list_cursor = await db.execute(stmt)
        truck_list = truck_list_cursor.fetchall()  # list[tuple[truck.id, truck.lat, truck.long]]

        stmt = select(CargoModel.id, CargoModel.pick_up_location, CargoModel.delivery_location, Location.latitude,
                      Location.longitude)
        stmt = stmt.join(Location, Location.zip_code == CargoModel.pick_up_location)  # noqa
        cargo_list_cursor = await db.execute(stmt)
        cargo_list = cargo_list_cursor.fetchall()  # list[tuple[cargo.id, cargo.lat, cargo.long]]

        cargo_dist_info = {}
        for cargo, pick_up, delivery, cargo_lat, cargo_long in cargo_list:
            truck_distance_info = []
            for truck, truck_lat, truck_long in truck_list:
                cargo_info = (cargo_lat, cargo_long)
                truck_info = (truck_lat, truck_long)
                distance = get_distance(cargo_info, truck_info)
                truck_distance_info.append(distance)
            logger.info(truck_distance_info)
            cargo_dist_info[cargo] = CargoWithTruckCountBase.parse_obj(
                {
                    'pick_up_location': pick_up,
                    'delivery_location': delivery,
                    'trucks': len(list(filter(lambda x: x <= 450, truck_distance_info)))
                }
            )

        return cargo_dist_info


cargo_crud = CRUDCargo(CargoModel)

# if __name__=='__main__':
#     import asyncio
#     from src.db.db import async_session
#     asyncio.run(cargo_crud.get_all_cargo_with_distance(db=async_session))
