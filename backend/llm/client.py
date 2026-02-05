import asyncio
from agents import Agent, Runner
from agents.tracing import set_tracing_disabled

from backend.config import MODEL_NAME
from backend.llm.prompt import SYSTEM_PROMPT

set_tracing_disabled(True)

agent = Agent(
    name="Blismos Academy Agent",
    model=MODEL_NAME,
    instructions=SYSTEM_PROMPT,
)

# -----------------------
# Non-streaming (used by /chat)
# -----------------------
async def generate_response(prompt: str) -> str:
    result = await Runner.run(agent, prompt)
    return result.final_output


# -----------------------
# Simulated streaming (used by /chat/stream)
# -----------------------
async def stream_response(prompt: str):
    """
    Simulated streaming for Agents SDK.
    Safe, production-ready, SDK-compatible.
    """

    result = await Runner.run(agent, prompt)
    text = result.final_output

    for word in text.split(" "):
        yield word + " "
        await asyncio.sleep(0.03)  # typing effect (tune this)
