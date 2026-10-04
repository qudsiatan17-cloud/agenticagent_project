"""
Writer Agent
------------
Takes all research findings and writes a clear structured answer.
Uses BALANCED model.
If Critic sends feedback, Writer improves the draft.
"""

from groq import Groq
from ..config import MODEL_BALANCED, GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM = """You are an expert writer.
Take the research notes and write a clear, well-structured answer.
Structure: Introduction → Main Points → Conclusion.
Write in simple clear language."""


def writer_node(state: dict) -> dict:
    notes = "\n\n".join(
        f"• {task}:\n  {finding}"
        for task, finding in state.get("research", {}).items()
    )

    critique_section = ""
    if state.get("critique") and state.get("revision_count", 0) > 0:
        critique_section = f"\n\nPrevious feedback to address:\n{state['critique']}"

    result = client.chat.completions.create(
        model=MODEL_BALANCED,
        max_tokens=900,
        messages=[
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": (
                    f"Question: {state['question']}\n\n"
                    f"Research notes:\n{notes}"
                    f"{critique_section}"
                )
            }
        ]
    )

    draft = result.choices[0].message.content.strip()
    rev = state.get("revision_count", 0)
    print(f"[Writer] Draft #{rev + 1} written")

    return {
        **state,
        "draft": draft,
        "revision_count": rev + 1,
        "agent_log": state.get("agent_log", []) + [f"[Writer] Draft #{rev + 1} written"]
    }
