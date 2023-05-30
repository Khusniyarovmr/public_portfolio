from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.cargo import (
    CargoCreate,
    CargoUpdate,
    CargoModelWithAllTrucks,
)
from services.crud.crud_cargo import cargo_crud
from services.crud.crud_locations import location_crud
from services.logger.logger import logger

cargo_router = APIRouter()


# - Удаление груза по ID.
@cargo_router.delete("/cargo", tags=["cargo"])
async def delete_cargo_by_id(
        *,
        db: AsyncSession = Depends(get_session),
        entity_in: int,
):
    """
       delete cargo by id.
    """

    await cargo_crud.delete(db=db, id=entity_in)
    return {'status': 200}


# - Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);
@cargo_router.post("/cargo", tags=["cargo"])
async def create_new_cargo(
        *,
        db: AsyncSession = Depends(get_session),
        entity_in: CargoCreate,
):
    """
    Create new cargo.
    """

    new_strategy = await cargo_crud.create(db=db, obj_in=entity_in)
    return new_strategy


# - Редактирование груза по ID (вес, описание);
@cargo_router.put("/cargo", tags=["cargo"])
async def update_cargo_by_id(
        *,
        db: AsyncSession = Depends(get_session),
        entity_in: CargoUpdate,
):
    """
       Update cargo by id.
    """
    current_cargo = await cargo_crud.get(db=db, id=entity_in.id)
    if current_cargo:
        new_strategy = await cargo_crud.update(db=db, db_obj=current_cargo, obj_in=entity_in)
        return new_strategy
    return {'status': 422, 'description': 'we dont have cargo by this id'}


# - Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание,
# список номеров ВСЕХ машин с расстоянием до выбранного груза);
@cargo_router.get("/cargo/id", tags=["cargo"], response_model=CargoModelWithAllTrucks)
async def get_cargo_by_id(
        *,
        db: AsyncSession = Depends(get_session),
        entity_in: int
):
    """
        Get cargo by id.
    """
    current_cargo = await cargo_crud.get(db=db, id=entity_in)
    if current_cargo:
        cargo_loc = await location_crud.get_lat_long_by_zip_code(db=db,
                                                                 zipcode=current_cargo.pick_up_location)
        logger.info(f'cargo_loc: {cargo_loc}')
        cargo_info = await cargo_crud.get_cargo_with_trucks(db=db, obj_in=entity_in, cargo_info=cargo_loc)
        return cargo_info
    return {'status': 422, 'description': 'cant find cargo'}


# - Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));
@cargo_router.get("/cargo", tags=["cargo"])
async def get_info_about_all_cargo(
        *,
        db: AsyncSession = Depends(get_session),
):
    """
        Get info about all cargo.
    """
    all_cargo_info = await cargo_crud.get_all_cargo_with_distance(db=db)
    return all_cargo_info
