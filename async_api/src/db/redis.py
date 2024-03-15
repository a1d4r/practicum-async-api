from core import config
from redis.asyncio import Redis

redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)


async def get_redis() -> Redis:
    return redis
