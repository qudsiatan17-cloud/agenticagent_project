"""
Orchestrator Agent
------------------
Reads the user question and decides which skill to use.
Uses the FAST model because this is just a classification task.
"""

from groq import Groq
from ..config import MODEL_FAST, GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
SKILLS = ["research", "calculate", "write"]


def orchestrator_node(state: dict) -> dict:
    question = state["question"]

    result = client.chat.completions.create(
        model=MODEL_FAST,
        max_tokens=10,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a routing agent. Classify the question into ONE of: "
                    "research, calculate, write. Reply with ONE word only."
                )
            },
            {"role": "user", "content": question}
        ]
    )

    route = result.choices[0].message.content.strip().lower()
    if route not in SKILLS:
        route = "research"

    print(f"[Orchestrator] Route → {route}")
    return {
        **state,
        "route": route,
        "agent_log": state.get("agent_log", []) + [f"[Orchestrator] Route → {route}"]
    }
