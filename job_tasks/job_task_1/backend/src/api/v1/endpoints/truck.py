from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db import get_session
from schemas.truck import (
    TruckModel,
    TruckUpdateById
)
from services.crud.crud_locations import location_crud
from services.crud.crud_truck import truck_crud

truck_router = APIRouter()


# Редактирование машины по ID (локация (определяется по введенному zip-коду));
@truck_router.put("/truck", tags=["truck"])
async def update_truck_by_id(
        *,
        db: AsyncSession = Depends(get_session),
        entity_in: TruckUpdateById,
) -> TruckModel | dict:
    """
       Update truck by id.
    """
    new_location = await location_crud.get_loc_by_zip_code(db, entity_in.zip_code)
    current_truck_model = await truck_crud.get(db=db, id=entity_in.id)
    if current_truck_model:
        new_truck_model = await truck_crud.update(db=db,
                                                  db_obj=current_truck_model,
                                                  obj_in={'current_location': new_location}
                                                  )
        return new_truck_model
    return {'status': 422}
