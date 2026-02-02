import redis.asyncio as redis
from config import REDIS_CONFIG

class RedisClient:
    def __init__(self):
        self.client: redis.Redis = None

    async def connect(self):
        config = REDIS_CONFIG.copy()
        config["decode_responses"] = True

        self.client = redis.Redis(**config)

    async def close(self):
        if self.client:
            await self.client.close()

# Redis 전역 인스턴스 생성
redis_client = RedisClient()