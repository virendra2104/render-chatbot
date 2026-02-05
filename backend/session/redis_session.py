import json
from typing import List
import redis.asyncio as redis

from agents.memory.session import SessionABC
from agents.items import TResponseInputItem


class RedisSession(SessionABC):
    """
    Redis-backed session for OpenAI Agents SDK
    """

    def __init__(
        self,
        session_id: str,
        redis_url: str = "redis://localhost:6379",
        ttl_seconds: int | None = None,
    ):
        self.session_id = session_id
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.key = f"agents:session:{session_id}"
        self.ttl = ttl_seconds

    async def get_items(
        self, limit: int | None = None
    ) -> List[TResponseInputItem]:
        data = await self.redis.lrange(self.key, 0, -1)
        items = [json.loads(item) for item in data]
        return items[-limit:] if limit else items

    async def add_items(
        self, items: List[TResponseInputItem]
    ) -> None:
        if not items:
            return

        pipe = self.redis.pipeline()
        for item in items:
            pipe.rpush(self.key, json.dumps(item))

        if self.ttl:
            pipe.expire(self.key, self.ttl)

        await pipe.execute()

    async def pop_item(self) -> TResponseInputItem | None:
        data = await self.redis.rpop(self.key)
        return json.loads(data) if data else None

    async def clear_session(self) -> None:
        await self.redis.delete(self.key)
