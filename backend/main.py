"""
main.py — FastAPI server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .pipeline import run_pipeline
from .memory   import get_all_memory

app = FastAPI(title="My AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    final_answer  : str
    quality_score : int
    route         : str
    agent_log     : list[str]


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    state = run_pipeline(req.question)
    return AskResponse(
        final_answer  = state.get("final_answer") or state.get("draft", "No answer."),
        quality_score = state.get("quality_score", 0),
        route         = state.get("route", ""),
        agent_log     = state.get("agent_log", [])
    )


@app.get("/memory")
def memory():
    """Return all saved memories"""
    return {"memories": get_all_memory()}


@app.get("/health")
def health():
    return {"status": "ok"}
