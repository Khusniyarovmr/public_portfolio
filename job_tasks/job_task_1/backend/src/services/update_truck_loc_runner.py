import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import async_session
from src.services.crud.crud_truck import truck_crud


class BackgroundRunner:
    def __init__(self, db):
        self.db: AsyncSession = db

    async def run_main(self):
        while True:
            await asyncio.sleep(180)
            await truck_crud.update_truck_location(self.db)


runner = BackgroundRunner(async_session)
