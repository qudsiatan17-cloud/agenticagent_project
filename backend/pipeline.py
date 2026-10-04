"""
pipeline.py — Connects all agents together
-------------------------------------------
Flow:
  Question
    → Orchestrator  (decides route)
    → Planner       (breaks into subtasks)
    → Researcher    (checks memory + searches web using ReAct)
    → Writer        (writes the answer)
    → Critic        (reviews — if bad, goes back to Writer)
    → Memory Save   (saves question + answer for future)
    → Final Answer
"""

from .agents.orchestrator import orchestrator_node
from .agents.planner      import planner_node
from .agents.researcher   import researcher_node
from .agents.writer       import writer_node
from .agents.critic       import critic_node
from .memory              import save_to_memory
from .config              import MIN_SCORE, MAX_REVISIONS


def run_pipeline(question: str) -> dict:
    """Run the full multi-agent pipeline and return the final state"""

    print("\n" + "="*60)
    print(f"  Question: {question}")
    print("="*60)

    # ── Initial state ─────────────────────────────────────
    state = {
        "question"      : question,
        "route"         : "",
        "subtasks"      : [],
        "research"      : {},
        "memory_context": [],
        "draft"         : "",
        "critique"      : "",
        "final_answer"  : "",
        "quality_score" : 0,
        "revision_count": 0,
        "agent_log"     : []
    }

    # ── Step 1: Orchestrator ──────────────────────────────
    state = orchestrator_node(state)

    # ── Step 2: Planner ───────────────────────────────────
    state = planner_node(state)

    # ── Step 3: Researcher (with memory) ─────────────────
    state = researcher_node(state)

    # ── Step 4: Writer + Critic loop ─────────────────────
    for attempt in range(MAX_REVISIONS + 1):
        state = writer_node(state)
        state = critic_node(state)

        if state.get("final_answer"):
            break

    # ── Step 5: Save to Memory ────────────────────────────
    if state.get("final_answer"):
        save_to_memory(
            question = question,
            answer   = state["final_answer"],
            score    = state.get("quality_score", 0)
        )
        state["agent_log"].append("[Memory] Answer saved for future use")

    print("\n" + "="*60)
    print("  DONE")
    print("="*60)

    return state
