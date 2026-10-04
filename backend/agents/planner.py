"""
Planner Agent
-------------
Reads the question and breaks it into 3 smaller subtasks.
Uses BALANCED model.
"""

import json
import re
from groq import Groq
from ..config import MODEL_BALANCED, GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def planner_node(state: dict) -> dict:
    question = state["question"]

    result = client.chat.completions.create(
        model=MODEL_BALANCED,
        max_tokens=200,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a task planner. Break the question into 3 specific subtasks. "
                    'Output ONLY a JSON array. Example: ["Find X", "Explain Y", "Compare Z"]'
                )
            },
            {"role": "user", "content": question}
        ]
    )

    text = result.choices[0].message.content
    match = re.search(r"\[.*?\]", text, re.DOTALL)

    try:
        subtasks = json.loads(match.group()) if match else [
            "Research the main topic",
            "Find examples",
            "Summarise key points"
        ]
    except Exception:
        subtasks = ["Research the main topic", "Find examples", "Summarise key points"]

    print(f"[Planner] Subtasks: {subtasks}")
    return {
        **state,
        "subtasks": subtasks,
        "agent_log": state.get("agent_log", []) + [f"[Planner] {len(subtasks)} subtasks created"]
    }
