"""
run.py — Easy way to test the agent from terminal
Run: python run.py
"""
import sys
sys.path.insert(0, ".")

from backend.pipeline import run_pipeline

print("\n🤖 My AI Agent — Multi-Agent System")
print("="*50)
print("Type your question and press Enter.")
print("Type 'quit' to exit.\n")

while True:
    question = input("You: ").strip()
    if not question:
        continue
    if question.lower() in ("quit", "exit"):
        print("Goodbye!")
        break

    state = run_pipeline(question)

    print("\n" + "="*50)
    print("FINAL ANSWER")
    print("="*50)
    print(state.get("final_answer") or state.get("draft", "No answer."))
    print(f"\nQuality Score: {state.get('quality_score', 0)}/10")
    print(f"Route: {state.get('route', '')}")
    print("="*50 + "\n")
