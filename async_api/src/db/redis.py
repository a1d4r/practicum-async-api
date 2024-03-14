from core import config
from redis.asyncio import Redis

redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)


class GetRedisError(Exception):
    def __init__(self, message: str = "Redis not found"):
        self.message = message


async def get_redis() -> Redis:
    if redis is None:
        raise GetRedisError
    return redis
