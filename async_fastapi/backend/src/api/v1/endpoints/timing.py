from fastapi import APIRouter
import time

timing_router = APIRouter()

@timing_router.get("/timing", tags=["timing"])
async def timing():
    time.sleep(5)
    return {"status": "OK"}
