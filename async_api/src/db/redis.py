# nfrom typing import Optional

from redis.asyncio import Redis

redis: Redis | None = None


class GetRedisError(Exception):
    def __init__(self, message: str = "Redis not found"):
        self.message = message


async def get_redis() -> Redis:
    if redis is None:
        raise GetRedisError
    return redis
