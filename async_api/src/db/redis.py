from core.settings import settings
from redis.asyncio import Redis

redis: Redis = Redis.from_url(str(settings.redis_url))


async def get_redis() -> Redis:
    return redis
