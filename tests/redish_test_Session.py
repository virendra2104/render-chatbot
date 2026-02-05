import asyncio
from agents import Agent, Runner
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.session.redis_session import RedisSession
from backend.config import MODEL_NAME

async def main():
    agent = Agent(
        name="Assistant",
        instructions="Reply very concisely.",
        model=MODEL_NAME
    )

    session = RedisSession(
        session_id="test_session_001",
        ttl_seconds=300,
    )

    # Turn 1
    result = await Runner.run(
        agent,
        "What city is the Golden Gate Bridge in?",
        session=session,
    )
    print(result.final_output)

    # Turn 2 (memory works)
    result = await Runner.run(
        agent,
        "What state is it in?",
        session=session,
    )
    print(result.final_output)

    # Turn 3
    result = await Runner.run(
        agent,
        "What's the population?",
        session=session,
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
