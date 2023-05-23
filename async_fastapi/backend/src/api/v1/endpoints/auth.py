from fastapi import APIRouter

from src.api.deps import fastapi_users
from src.schemas.auth import UserCreate, UserRead, UserUpdate
from src.services.auth.auth import cookie_backend

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(cookie_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
