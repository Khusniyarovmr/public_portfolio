from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.location import Location as LocationModel
from src.schemas.location import LocationCreate, LocationUpdate
from src.services.crud.base import RepositoryDB


class CRUDLocations(RepositoryDB[LocationModel, LocationCreate, LocationUpdate]):

    @staticmethod
    async def get_loc_by_zip_code(db: AsyncSession, zipcode: str):
        stmt = select(LocationModel.id).where(LocationModel.zip_code == zipcode)
        location_cursor = await db.execute(stmt)
        loc_id = location_cursor.scalar()
        return loc_id

    @staticmethod
    async def get_lat_long_by_zip_code(db: AsyncSession, zipcode: str):
        stmt = select(LocationModel.latitude, LocationModel.longitude).where(LocationModel.zip_code == zipcode)
        location_cursor = await db.execute(stmt)
        loc_info = location_cursor.all()
        return loc_info[0]


location_crud = CRUDLocations(LocationModel)

# if __name__=='__main__':
#     import asyncio
#     from src.db.db import async_session
#     asyncio.run(location_crud.get_lat_long_by_zip_code(db=async_session, zipcode='02702'))
