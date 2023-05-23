from http import HTTPStatus

from fastapi import APIRouter, Depends, Request, Response
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import MissingTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import deps
from src.db.db import get_session
from src.models.user import User
from src.schemas.strategy_tp_and_sl import (
    StrategyTPAndSLUpdate,
)
from src.schemas.user_trade_strategy import (
    UserTradeStrategyCreate,
    UserTradeStrategyUpdate,
    UserTradeStrategyWithSymbol
)
from src.services.crud.crud_strategy_tp_and_sl import strategy_tp_and_sl_crud
from src.services.crud.crud_user_trade_strategy import user_trade_strategy_crud
from src.services.utilities.publisher import publisher

user_ts_router = APIRouter()


@user_ts_router.post("/strategy",
                     tags=["strategy"],
                     response_model=UserTradeStrategyWithSymbol,
                     response_model_exclude_unset=True
                     )
async def add_user_strategy(
        *,
        request: Request,
        db: AsyncSession = Depends(get_session),
        entity_in: UserTradeStrategyCreate,
        current_user: User = Depends(deps.get_current_autorize_user),
        csrf_protect: CsrfProtect = Depends()
):
    """
    Create new personal user strategy.
    """
    try:
        csrf_protect.validate_csrf_in_cookies(request)
    except MissingTokenError:
        return Response(status_code=HTTPStatus.FORBIDDEN)

    if current_user:
        entity_in.user_id = current_user.id
        new_strategy = await user_trade_strategy_crud.create(db=db, obj_in=entity_in)
        publisher('strategy', new_strategy)
        return new_strategy


@user_ts_router.get("/strategy/active", tags=["strategy"])
async def get_user_strategy_active(
        *,
        db: AsyncSession = Depends(get_session),
        current_user: User = Depends(deps.get_current_autorize_user)
):
    """
        Get all personal and active user strategies.
    """
    if current_user:
        new_strategy = await user_trade_strategy_crud.get_all_active_strategies(db=db, user_id=current_user.id)
        return new_strategy


@user_ts_router.get("/strategy/history", tags=["strategy"])
async def get_user_strategy_history(
        *,
        db: AsyncSession = Depends(get_session),
        current_user: User = Depends(deps.get_current_autorize_user)
):
    """
        Get all personal user strategies.
    """
    if current_user:
        new_strategy = await user_trade_strategy_crud.get_all_strategies(db=db, user_id=current_user.id)
        return new_strategy


@user_ts_router.put("/strategy", tags=["strategy"])
async def update_user_strategy(
        *,
        request: Request,
        db: AsyncSession = Depends(get_session),
        entity_in: UserTradeStrategyUpdate,
        current_user: User = Depends(deps.get_current_autorize_user),
        csrf_protect: CsrfProtect = Depends()
):
    """
       Update personal user strategy by id.
    """
    try:
        csrf_protect.validate_csrf_in_cookies(request)
    except MissingTokenError:
        return Response(status_code=HTTPStatus.FORBIDDEN)
    if current_user:
        entity_in.user_id = current_user.id
        current_strategy = await user_trade_strategy_crud.get(db=db, id=entity_in.id)
        new_strategy = await user_trade_strategy_crud.update(db=db, db_obj=current_strategy, obj_in=entity_in)
        publisher('strategy', new_strategy)
        return new_strategy


@user_ts_router.delete("/strategy/delete", tags=["strategy"])
async def delete_user_strategy(
        *,
        request: Request,
        db: AsyncSession = Depends(get_session),
        entity_in: int,
        current_user: User = Depends(deps.get_current_autorize_user),
        csrf_protect: CsrfProtect = Depends()
):
    """
       delete personal user strategy by id.
    """
    try:
        csrf_protect.validate_csrf_in_cookies(request)
    except MissingTokenError:
        return Response(status_code=HTTPStatus.FORBIDDEN)
    if current_user:
        pub_data = {
            'user_id': current_user.id,
            'event_type': 'delete',
            'modify_obj': {
                'name': 'strategy',
                'data': entity_in
            }
        }
        publisher('event', pub_data)
        await user_trade_strategy_crud.delete(db=db, id=entity_in)
        return {'status': 200}


@user_ts_router.post("/strategy/tpsl",
                     tags=["strategy"]
                     )
async def add_strategy_tp_and_sl(
        *,
        request: Request,
        db: AsyncSession = Depends(get_session),
        entity_in: list[StrategyTPAndSLUpdate],
        current_user: User = Depends(deps.get_current_autorize_user),
        csrf_protect: CsrfProtect = Depends()
):
    """
    add tp and sl to strategy.
    """
    try:
        csrf_protect.validate_csrf_in_cookies(request)
    except MissingTokenError:
        return Response(status_code=HTTPStatus.FORBIDDEN)
    if current_user:
        strategy_tp_and_sl = await strategy_tp_and_sl_crud.add_or_update_tp_and_sl(db=db, obj_in=entity_in)
        publisher('strategy_tp_and_sl', strategy_tp_and_sl)
        return strategy_tp_and_sl


@user_ts_router.delete("/strategy/tpsl_del",
                       tags=["strategy"]
                       )
async def delete_strategy_tp_and_sl(
        *,
        request: Request,
        db: AsyncSession = Depends(get_session),
        entity_in: int,
        current_user: User = Depends(deps.get_current_autorize_user),
        csrf_protect: CsrfProtect = Depends()
):
    """
    delete tp and sl to strategy.
    """
    try:
        csrf_protect.validate_csrf_in_cookies(request)
    except MissingTokenError:
        return Response(status_code=HTTPStatus.FORBIDDEN)
    if current_user:
        pub_data = {
            'user_id': current_user.id,
            'event_type': 'delete',
            'modify_obj': {
                'name': 'strategy_tp_and_sl',
                'data': entity_in
            }
        }
        publisher('event', pub_data)
        await strategy_tp_and_sl_crud.delete(db=db, id=entity_in)
        return {'status': 200}
