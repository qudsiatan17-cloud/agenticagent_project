"""
memory.py — Simple Memory System
----------------------------------
Saves every question + answer to a JSON file.
When a new question comes in, retrieves similar past answers.

This is a simple version of what ChromaDB/vector databases do.
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Memory file location
MEMORY_FILE = Path(__file__).parent.parent / "memory.json"


def save_to_memory(question: str, answer: str, score: int):
    """Save a question and answer to memory"""
    
    # Load existing memory
    memory = _load_memory()
    
    # Add new entry
    memory.append({
        "question" : question,
        "answer"   : answer[:500],   # save first 500 chars
        "score"    : score,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 20 entries
    memory = memory[-20:]
    
    # Save back to file
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)
    
    print(f"[Memory] Saved! Total memories: {len(memory)}")


def retrieve_from_memory(question: str, top_k: int = 3) -> list[dict]:
    """Find past answers that are similar to the current question"""
    
    memory = _load_memory()
    if not memory:
        return []
    
    # Simple keyword matching
    # (A real system would use vector embeddings)
    question_words = set(question.lower().split())
    scored = []
    
    for entry in memory:
        past_words = set(entry["question"].lower().split())
        # Count how many words match
        common = len(question_words & past_words)
        if common > 0:
            scored.append((common, entry))
    
    # Sort by most matching words
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Return top_k results
    results = [entry for _, entry in scored[:top_k]]
    print(f"[Memory] Retrieved {len(results)} past answer(s)")
    return results


def _load_memory() -> list:
    """Load memory from file"""
    if not MEMORY_FILE.exists():
        return []
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def get_all_memory() -> list:
    """Return all saved memories"""
    return _load_memory()
