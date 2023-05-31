import redis.asyncio as aioredis

from core.config import app_settings

aio_redis = aioredis.Redis(host=app_settings.HOST,
                           port=app_settings.PORT,
                           db=0,
                           decode_responses=True
                           )
