"""FastAPI backend service for AI Financial Advisor Bot."""

import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from advisor_agents import LOG_FILE, run_query

app = FastAPI(
    title="AI Financial Advisor Bot API",
    description="Multi-agent financial advisory API powered by Groq and OpenAI Agents SDK.",
)

# CORS allowing all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/", include_in_schema=False)
def root():
    """Redirect root path to interactive API docs."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    """Health check endpoint for hosting platforms."""
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    """Process a financial question and return the agent response."""
    return run_query(request.message)


@app.get("/handoffs")
def get_handoffs():
    """Return the last 20 logged agent handoffs as a JSON list."""
    if not os.path.exists(LOG_FILE):
        return []

    lines = []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except Exception:
        return []

    recent_lines = lines[-20:]
    handoffs = []
    for line in recent_lines:
        try:
            handoffs.append(json.loads(line))
        except Exception:
            pass

    return handoffs
