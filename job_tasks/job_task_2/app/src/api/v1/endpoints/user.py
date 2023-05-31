from fastapi import APIRouter

from schemas.user import UserModel
from services.crud.user import crud_user

user_router = APIRouter()


@user_router.post("/write_data", tags=["user"])
async def create_user_by_phone(
        *,
        entity_in: UserModel,
):
    """
    Create new user.
    """
    create_result = await crud_user.create_user_by_phone(obj_in=entity_in)
    return create_result


@user_router.put("/write_data", tags=["user"])
async def update_address_by_phone(
        *,
        entity_in: UserModel,
):
    """
       Update address by phone number.
    """
    update_result = await crud_user.update_address_by_phone(obj_in=entity_in)
    return update_result


@user_router.get("/check_data", tags=["user"], response_model=UserModel | dict)
async def get_address_by_phone(
        *,
        entity_in: str
):
    """
        Get user address by phone number.
    """
    user_address = await crud_user.get_address_by_phone(phone=entity_in)
    return user_address
