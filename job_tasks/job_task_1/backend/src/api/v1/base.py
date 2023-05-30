from fastapi import APIRouter

from src.api.v1.endpoints.cargo import cargo_router
from src.api.v1.endpoints.init_db_data import init_db_data_router
from src.api.v1.endpoints.truck import truck_router

api_router = APIRouter()
api_router.include_router(init_db_data_router)
api_router.include_router(truck_router)
api_router.include_router(cargo_router)
