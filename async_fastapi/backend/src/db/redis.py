import redis.asyncio as aioredis
import redis

aio_redis = aioredis.Redis(host='localhost', port=6379, db=0)
st_redis = redis.Redis(host='localhost', port=6379, db=0)
