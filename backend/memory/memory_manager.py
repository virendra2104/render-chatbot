WINDOW_SIZE = 6
MAX_MESSAGES = 20

class MemoryManager:
    def __init__(self, store):
        self.store = store

    async def build_context(self, session_id: str) -> str:
        session = await self.store.get(session_id)

        messages = session["messages"]
        summary = session.get("summary", "")

        parts = []

        if summary:
            parts.append(f"Conversation summary:\n{summary}")

        for msg in messages[-WINDOW_SIZE:]:
            parts.append(f'{msg["role"]}: {msg["content"]}')

        return "\n".join(parts)

    async def add_message(self, session_id: str, role: str, content: str):
        session = await self.store.get(session_id)

        session["messages"].append({
            "role": role,
            "content": content
        })

        if len(session["messages"]) > MAX_MESSAGES:
            session["messages"] = session["messages"][-MAX_MESSAGES:]

        await self.store.save(session_id, session)
