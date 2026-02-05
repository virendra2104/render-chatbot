# backend/llm/session.py
import asyncio
from agents import Agent, Runner, SQLiteSession
from backend.config import MODEL_NAME
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
    model=MODEL_NAME,
)

session = SQLiteSession("conversation_123")


async def main():
    # First turn
    result = await Runner.run(
        agent,
        "What city is has BHU?",
        session=session
    )
    print(result.final_output)

    # Second turn
    result = await Runner.run(
        agent,
        "What state is it in?",
        session=session
    )
    print(result.final_output)

    # Third turn (ASYNC, not sync)
    result = await Runner.run(
        agent,
        "What's the population?",
        session=session
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
