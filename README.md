<<<<<<< HEAD
# 🤖 My AI Agent — Multi-Agent System

A simple multi-agent AI system using all core Agentic AI concepts:
- **Orchestrator** — routes your question to the right skill
- **Planner** — breaks your question into subtasks
- **Researcher** — uses ReAct loop to search the web
- **Writer** — writes a structured answer
- **Critic** — reviews and improves the answer

---

## Concepts Used
| Concept | Where |
|---|---|
| ReAct (Reason + Act) | `backend/agents/researcher.py` |
| Tool Use / Function Calling | `backend/tools.py` |
| Multi-Agent Pipeline | `backend/pipeline.py` |
| Orchestration / Routing | `backend/agents/orchestrator.py` |
| Self-Critique / Revision | `backend/agents/critic.py` |
| Fast vs Balanced Models | `backend/config.py` |
| REST API | `backend/main.py` |

---

## Setup

### 1. Install packages
```
pip install -r requirements.txt
pip install duckduckgo-search
```

### 2. Create .env file
Copy `.env.example` to `.env` and add your key:
```
ANTHROPIC_API_KEY=your_key_here
```

### 3. Run from terminal (simple)
```
python run.py
```

### 4. Run with web UI
**Terminal 1 — Backend:**
```
uvicorn backend.main:app --reload --port 9000
```

**Terminal 2 — Frontend:**
Just open `frontend/index.html` in your browser!

---

## Project Structure
```
myproject/
├── .env                  ← Your API key (create this)
├── .env.example          ← Template
├── requirements.txt      ← Python packages
├── run.py                ← Quick terminal test
├── frontend/
│   └── index.html        ← Web UI
└── backend/
    ├── config.py         ← All settings
    ├── tools.py          ← web_search, calculator
    ├── pipeline.py       ← Connects all agents
    ├── main.py           ← FastAPI server
    └── agents/
        ├── orchestrator.py
        ├── planner.py
        ├── researcher.py
        ├── writer.py
        └── critic.py
```


