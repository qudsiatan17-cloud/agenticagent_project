"""
Critic Agent
------------
Reviews the Writer's draft and gives a score out of 10.
If score is too low, sends back to Writer for improvement.
Uses FAST model.
"""

import re
from groq import Groq
from ..config import MODEL_FAST, GROQ_API_KEY, MIN_SCORE, MAX_REVISIONS

client = Groq(api_key=GROQ_API_KEY)

SYSTEM = (
    "You are a strict quality reviewer. Evaluate the answer and reply ONLY in this format:\n"
    "Score: X/10\n"
    "Strengths: <one sentence>\n"
    "Weaknesses: <one sentence>\n"
    "Verdict: PASS or REVISE"
)


def critic_node(state: dict) -> dict:
    result = client.chat.completions.create(
        model=MODEL_FAST,
        max_tokens=150,
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"Question: {state['question']}\n\nAnswer:\n{state['draft']}"
            }
        ]
    )

    review = result.choices[0].message.content.strip()

    try:
        score = int(re.search(r"Score:\s*(\d+)", review).group(1))
    except Exception:
        score = 7

    print(f"[Critic] Score: {score}/10")

    updates = {
        **state,
        "critique": review,
        "quality_score": score,
        "agent_log": state.get("agent_log", []) + [f"[Critic] Score {score}/10"]
    }

    passes = score >= MIN_SCORE or state.get("revision_count", 0) >= MAX_REVISIONS
    if passes:
        updates["final_answer"] = state["draft"]
        print("[Critic] PASS ✓")
    else:
        print("[Critic] REVISE — sending back to Writer")

    return updates
