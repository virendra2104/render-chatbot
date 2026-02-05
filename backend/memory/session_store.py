import json
import redis.asyncio as redis
from typing import Dict

class RedisSessionStore:
    def __init__(self, redis_url: str, ttl: int = 3600):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.ttl = ttl

    def _key(self, session_id: str) -> str:
        return f"session:{session_id}"

    async def get(self, session_id: str) -> Dict:
        raw = await self.redis.get(self._key(session_id))
        if not raw:
            return {"messages": [], "summary": ""}
        return json.loads(raw)

    async def save(self, session_id: str, data: Dict):
        await self.redis.set(
            self._key(session_id),
            json.dumps(data),
            ex=self.ttl
        )

    async def clear(self, session_id: str):
        await self.redis.delete(self._key(session_id))
