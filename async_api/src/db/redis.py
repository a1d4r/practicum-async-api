from redis.asyncio import Redis

from core.settings import settings

redis: Redis = Redis.from_url(str(settings.redis_url))


async def get_redis() -> Redis:
    return redis
