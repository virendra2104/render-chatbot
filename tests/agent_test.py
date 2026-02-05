import asyncio
import sys
import os

# -------------------------------------------------
# Add project root to PYTHONPATH
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.llm.client import generate_response


async def main():
    response = await generate_response("list courses")
    print("\nBlismos Academy AI Response:\n")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
