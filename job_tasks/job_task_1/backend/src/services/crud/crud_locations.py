from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.location import Location as LocationModel
from schemas.location import LocationCreate, LocationUpdate
from services.crud.base import RepositoryDB


class CRUDLocations(RepositoryDB[LocationModel, LocationCreate, LocationUpdate]):

    @staticmethod
    async def get_loc_by_zip_code(db: AsyncSession, zipcode: str) -> int:
        stmt = select(LocationModel.id).where(LocationModel.zip_code == zipcode)
        location_cursor = await db.execute(stmt)
        loc_id = location_cursor.scalar()
        return loc_id

    @staticmethod
    async def get_lat_long_by_zip_code(db: AsyncSession, zipcode: str) -> tuple:
        stmt = select(LocationModel.latitude, LocationModel.longitude).where(LocationModel.zip_code == zipcode)
        location_cursor = await db.execute(stmt)
        loc_info = location_cursor.all()
        return loc_info[0]


location_crud = CRUDLocations(LocationModel)
