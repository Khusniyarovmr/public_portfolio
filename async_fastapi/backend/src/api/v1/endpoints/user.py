from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import MissingTokenError
from http import HTTPStatus

from src.api import deps
from src.db.db import get_session
from src.models.user import User
from src.schemas.user_settings import UserSettingsCreate, UserSettingsUpdate
from src.services.crud.crud_user_settings import user_settings_crud
from src.services.logger.logger import logger

user_router = APIRouter()


@user_router.post("/user/settings", tags=["users"])
async def add_user_settings(
        *,
        request: Request,
        db: AsyncSession = Depends(get_session),
        entity_in: UserSettingsCreate,
        current_user: User = Depends(deps.get_current_autorize_user),
        csrf_protect: CsrfProtect = Depends()
):
    """
    Add new user binance API info.
    """
    try:
        csrf_protect.validate_csrf_in_cookies(request)
    except MissingTokenError:
        return Response(status_code=HTTPStatus.FORBIDDEN)
    logger.info(f'we have entity: {entity_in}')
    if current_user:
        entity_in.user_id = current_user.id
        new_strategy = await user_settings_crud.create(db=db, obj_in=entity_in)
        return new_strategy
