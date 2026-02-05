# backend/api/chat.py
from fastapi.responses import StreamingResponse
import asyncio
from backend.llm.client import stream_response
from backend.mcp_google_sheets.registration import register_user
from fastapi import APIRouter, Header, Depends, HTTPException
from pydantic import BaseModel
from backend.mcp_google_sheets.registration import register_user

from backend.memory.session_store import RedisSessionStore
from backend.memory.memory_manager import MemoryManager
from backend.llm.client import generate_response

from backend.security.auth import verify_token
from backend.security.rate_limit import rate_limit
from backend.security.sanitize import sanitize_input, sanitize_output
from backend.mcp_google_sheets.intent_detector import detect_intent

from backend.config import REDIS_URL

router = APIRouter()
# 👇 ADD HERE
CANCEL_COMMANDS = {"cancel", "stop", "exit", "quit"}
RESTART_COMMANDS = {"restart", "reset", "start over", "start again"}
# -----------------------
# Memory setup (Redis)
# -----------------------
store = RedisSessionStore(REDIS_URL)
memory = MemoryManager(store)

class RegistrationRequest(BaseModel):
    name: str
    phone: str
    email: str
    course: str

@router.post("/register")
async def register(
    payload: RegistrationRequest,
    session_id: str = Header(..., alias="X-Session-ID")
):
    """
    Store user registration in Google Sheet
    """
    user_data = payload.dict()
    response = register_user(user_data)
    return {"response": response}
# -----------------------
# Request schema
# -----------------------
class ChatRequest(BaseModel):
    message: str


# -----------------------
# Chat endpoint
# -----------------------
@router.post("/chat")
async def chat(
    payload: ChatRequest,
    session_id: str = Header(..., alias="X-Session-ID"),
    token_data: dict = Depends(verify_token),
):
    await rate_limit(token_data["sub"])

    # Sanitize input
    try:
        message = sanitize_input(payload.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Load session data
    session_data = await store.get(session_id)

    # Detect intent
    intent = session_data.get("intent") or detect_intent(message)

    # ==================================================
    # REGISTRATION FLOW
    # ==================================================
    if intent == "REGISTER":
        session_data["intent"] = "REGISTER"

        registration = session_data.get(
            "registration",
            {
                "name": None,
                "phone": None,
                "email": None,
                "course": None,
            }
        )

        registration_started = session_data.get("registration_started", False)

        # ---- first registration message ----
        if not registration_started:
            session_data["registration_started"] = True
            session_data["registration"] = registration
            await store.save(session_id, session_data)

            return {"response": "Please provide your name"}

        # ---- slot filling ----
        if not registration["name"]:
            registration["name"] = message.strip()

        elif not registration["phone"]:
            registration["phone"] = message.strip()

        elif not registration["email"]:
            registration["email"] = message.strip()

        elif not registration["course"]:
            registration["course"] = message.strip()

        session_data["registration"] = registration
        await store.save(session_id, session_data)

        missing = [k for k, v in registration.items() if not v]

        if missing:
            return {"response": f"Please provide your {missing[0]}"}

        # ---- save to Google Sheets ----
        result = register_user(registration)

        await store.clear(session_id)

        return {"response": result}

    # ==================================================
    # NORMAL CHAT FLOW
    # ==================================================
    context = await memory.build_context(session_id)

    final_prompt = f"""
{context}

user: {message}
assistant:
""".strip()

    response = await generate_response(final_prompt)
    response = sanitize_output(response)

    await memory.add_message(session_id, "user", message)
    await memory.add_message(session_id, "assistant", response)

    return {"response": response}


@router.post("/chat/stream")
async def chat_stream(
    payload: ChatRequest,
    session_id: str = Header(..., alias="X-Session-ID"),
    token_data: dict = Depends(verify_token),
):
    await rate_limit(token_data["sub"])

    try:
        message = sanitize_input(payload.message)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    session_data = await store.get(session_id)
    intent = session_data.get("intent") or detect_intent(message)

    text = message.lower().strip()

    # ==================================================
    # REGISTRATION FLOW (PLAIN TEXT ONLY)
    # ==================================================
    if intent == "REGISTER":
        session_data["intent"] = "REGISTER"

        # ---- cancel ----
        if text in CANCEL_COMMANDS:
            await store.clear(session_id)
            return StreamingResponse(
                iter(["Registration cancelled. How else can I help you?"]),
                media_type="text/plain",
            )

        # ---- restart ----
        if text in RESTART_COMMANDS:
            session_data = {
                "intent": "REGISTER",
                "registration_started": False,
                "registration": {
                    "name": None,
                    "phone": None,
                    "email": None,
                    "course": None,
                },
            }
            await store.save(session_id, session_data)
            return StreamingResponse(
                iter(["Registration restarted. Please provide your name."]),
                media_type="text/plain",
            )

        registration = session_data.get(
            "registration",
            {"name": None, "phone": None, "email": None, "course": None}
        )

        if not session_data.get("registration_started"):
            session_data["registration_started"] = True
            session_data["registration"] = registration
            await store.save(session_id, session_data)
            return StreamingResponse(
                iter(["Please provide your name"]),
                media_type="text/plain",
            )

        if not registration["name"]:
            registration["name"] = message.strip()
        elif not registration["phone"]:
            registration["phone"] = message.strip()
        elif not registration["email"]:
            registration["email"] = message.strip()
        elif not registration["course"]:
            registration["course"] = message.strip()

        session_data["registration"] = registration
        await store.save(session_id, session_data)

        missing = [k for k, v in registration.items() if not v]
        if missing:
            return StreamingResponse(
                iter([f"Please provide your {missing[0]}"]),
                media_type="text/plain",
            )

        result = register_user(registration)
        await store.clear(session_id)

        return StreamingResponse(
            iter([result]),
            media_type="text/plain",
        )

    # ==================================================
    # NORMAL STREAMING CHAT
    # ==================================================
    context = await memory.build_context(session_id)

    final_prompt = f"""
{context}

user: {message}
assistant:
""".strip()

    async def event_generator():
        collected = []
        async for chunk in stream_response(final_prompt):
            collected.append(chunk)
            yield chunk
            await asyncio.sleep(0)

        final_text = sanitize_output("".join(collected))
        await memory.add_message(session_id, "user", message)
        await memory.add_message(session_id, "assistant", final_text)

    return StreamingResponse(event_generator(), media_type="text/plain")
