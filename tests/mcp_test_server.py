import asyncio
from agents import Agent, Runner
from agents.tracing import set_tracing_disabled
import asyncio
from agents import Agent, Runner
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.session.redis_session import RedisSession
from backend.config import MODEL_NAME
set_tracing_disabled(True)

agent = Agent(
    name="Test Agent",
    instructions="You are a helpful assistant.",
    model=MODEL_NAME,
    mcp_servers=[],  # No MCP to avoid errors
)

async def main():
    result = await Runner.run(agent, "What is a string in Python?")
    print(result.final_output)  # ✅ use final_output instead of final

asyncio.run(main())