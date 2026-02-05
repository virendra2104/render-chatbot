FORBIDDEN_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "act as",
    "developer message",
]

def sanitize_input(text: str) -> str:
    lowered = text.lower()
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in lowered:
            raise ValueError("Potential prompt injection detected")
    return text.strip()

def sanitize_output(text: str) -> str:
    if not text:
        return text

    # normalize spaces BUT keep line breaks
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)

