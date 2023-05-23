from fastapi import Depends, HTTPException
from fastapi_users import FastAPIUsers

from src.models.user import User
from src.services.auth.auth import cookie_backend
from src.services.auth.manager import get_user_manager
from src.services.crud.user import user_crud

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [cookie_backend],
)

current_active_user = fastapi_users.current_user(active=True)


async def get_current_active_user(
        current_user: User = Depends(current_active_user),
) -> User:
    if not await user_crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
        current_user: User = Depends(current_active_user),
) -> User:
    if not user_crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_autorize_user(
        current_user: User = Depends(current_active_user),
) -> User:
    if not user_crud.is_autorized(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
