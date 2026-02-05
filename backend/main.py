from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.api.chat import router as chat_router

app = FastAPI(title="Blismos Academy AI")

# Include backend API
app.include_router(chat_router)

# CORS (optional if frontend is separate origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)
# Serve frontend folder
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

