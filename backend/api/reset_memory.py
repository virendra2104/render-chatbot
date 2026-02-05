from fastapi import APIRouter, Header, Depends
from backend.memory.session_store import RedisSessionStore
from backend.security.auth import verify_token
from backend.config import REDIS_URL

router = APIRouter()

store = RedisSessionStore(REDIS_URL)

@router.post("/reset_memory")
async def reset_memory(
    session_id: str = Header(..., alias="X-Session-ID"),
    _: dict = Depends(verify_token),
):
    await store.clear(session_id)
    return {"status": "memory reset successful"}
