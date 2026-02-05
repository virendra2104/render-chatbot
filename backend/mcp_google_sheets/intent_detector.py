def detect_intent(message: str) -> str:
    message = message.lower()

    register_keywords = [
        "register",
        "registration",
        "enroll",
        "sign up",
        "admission"
    ]

    for word in register_keywords:
        if word in message:
            return "REGISTER"

    return "CHAT"
