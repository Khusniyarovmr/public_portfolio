from fastapi import APIRouter

from src.api.v1.endpoints.auth import auth_router
from src.api.v1.endpoints.web_hook import web_hook_router
from src.api.v1.endpoints.strategy import user_ts_router
from src.api.v1.endpoints.csrf import csrf_router
from src.api.v1.endpoints.timing import timing_router
from src.api.v1.endpoints.user import user_router


api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(web_hook_router)
api_router.include_router(user_ts_router)
api_router.include_router(csrf_router)
api_router.include_router(timing_router)
api_router.include_router(user_router)
