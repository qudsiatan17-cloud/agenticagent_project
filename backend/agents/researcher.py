"""
Researcher Agent — ReAct Pattern
---------------------------------
Now uses Memory! Before searching the web, checks if we already
answered something similar before.

Flow:
  1. Check memory for similar past answers
  2. Search web for new information
  3. Combine memory + web results
  4. Summarise findings
"""

from groq import Groq
from ..config import MODEL_BALANCED, GROQ_API_KEY, MAX_REACT_STEPS
from ..tools import web_search
from ..memory import retrieve_from_memory

client = Groq(api_key=GROQ_API_KEY)


def researcher_node(state: dict) -> dict:
    findings = {}

    # ── Step 1: Check Memory first ────────────────────────
    past_answers = retrieve_from_memory(state["question"])
    memory_context = ""
    if past_answers:
        memory_context = "\n\nRelevant past answers from memory:\n" + "\n".join(
            f"- Q: {m['question']}\n  A: {m['answer'][:200]}"
            for m in past_answers
        )
        print(f"[Researcher] Found {len(past_answers)} memory match(es)")

    for subtask in state.get("subtasks", []):
        print(f"[Researcher] Working on: {subtask}")

        # Step 2 — Ask Groq what to search for
        search_query_resp = client.chat.completions.create(
            model=MODEL_BALANCED,
            max_tokens=50,
            messages=[
                {
                    "role": "system",
                    "content": "You are a research assistant. Given a subtask, reply with ONLY a short web search query (5 words max)."
                },
                {"role": "user", "content": f"Subtask: {subtask}"}
            ]
        )
        query = search_query_resp.choices[0].message.content.strip()
        print(f"[Researcher] Searching: {query}")

        # Step 3 — Search the web
        search_result = web_search(query)
        print(f"[Researcher] Got results: {search_result[:100]}...")

        # Step 4 — Summarise combining web + memory
        summary_resp = client.chat.completions.create(
            model=MODEL_BALANCED,
            max_tokens=300,
            messages=[
                {
                    "role": "system",
                    "content": "You are a research assistant. Summarise the search results in 3-4 clear sentences relevant to the subtask. If memory context is provided, use it too."
                },
                {
                    "role": "user",
                    "content": (
                        f"Subtask: {subtask}\n\n"
                        f"Search results:\n{search_result}"
                        f"{memory_context}"
                    )
                }
            ]
        )
        findings[subtask] = summary_resp.choices[0].message.content.strip()
        print(f"[Researcher] Done: {subtask[:50]}...")

    return {
        **state,
        "memory_context": [m["answer"] for m in past_answers],
        "research"      : findings,
        "agent_log"     : state.get("agent_log", []) + [
            f"[Researcher] {len(findings)} findings, {len(past_answers)} from memory"
        ]
    }
