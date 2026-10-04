"""
config.py — All settings in one place
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[1] / ".env")

# ── API Key ───────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ── Models ────────────────────────────────────────────────
MODEL_FAST     = "llama-3.1-8b-instant"   # Fast cheap model  → Orchestrator, Critic
MODEL_BALANCED = "llama-3.3-70b-versatile" # Balanced model → Planner, Researcher, Writer

# ── Agent settings ────────────────────────────────────────
MAX_REACT_STEPS = 5    # How many times Researcher can call tools
MAX_REVISIONS   = 2    # How many times Critic can send back to Writer
MIN_SCORE       = 7    # Critic score needed to pass (out of 10)
