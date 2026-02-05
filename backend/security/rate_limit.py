import time
import redis.asyncio as redis
from fastapi import HTTPException, status

from backend.config import REDIS_URL, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW

print("DEBUG REDIS_URL =", repr(REDIS_URL))   # 👈 ADD THIS LINE

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def rate_limit(identifier: str):
    key = f"rate:{identifier}"
    now = int(time.time())

    pipe = redis_client.pipeline()
    pipe.zadd(key, {now: now})
    pipe.zremrangebyscore(key, 0, now - RATE_LIMIT_WINDOW)
    pipe.zcard(key)
    pipe.expire(key, RATE_LIMIT_WINDOW)
    _, _, count, _ = await pipe.execute()

    if count > RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )

