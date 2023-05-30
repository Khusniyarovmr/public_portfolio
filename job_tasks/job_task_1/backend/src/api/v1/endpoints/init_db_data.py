import asyncio

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import async_session
from src.services.crud.crud_init_db import insert_loc_from_file, insert_trucks_on_init
from src.services.update_truck_loc_runner import runner

init_db_data_router = APIRouter()


@init_db_data_router.on_event("startup")
async def on_startup(
        *,
        db: AsyncSession = async_session,
):
    await insert_loc_from_file(db)
    await insert_trucks_on_init(db)


@init_db_data_router.on_event('startup')
async def app_startup():
    asyncio.create_task(runner.run_main())
