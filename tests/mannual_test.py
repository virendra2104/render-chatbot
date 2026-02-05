import asyncio
import sys
import os

# -------------------------------------------------
# Add project root to PYTHONPATH
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
import asyncio
from backend.llm.client import generate_response
from backend.memory.session_store import RedisSessionStore
from backend.memory.memory_manager import MemoryManager

async def test_agent():
    response = await generate_response("Hello, who are you?")
    print("AGENT RESPONSE:\n", response)

async def test_memory():
    store = RedisSessionStore("redis://localhost:6379")
    memory = MemoryManager(store)

    session_id = "test-session-1"

    await memory.add_message(session_id, "user", "Hi")
    await memory.add_message(session_id, "assistant", "Hello!")

    context = await memory.build_context(session_id)
    print("\nMEMORY CONTEXT:\n", context)

async def main():
    await test_agent()
    await test_memory()

if __name__ == "__main__":
    asyncio.run(main())
