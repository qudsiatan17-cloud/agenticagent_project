"""
tools.py — Real tools the Researcher agent can call
"""

def web_search(query: str) -> str:
    """Search the web using DuckDuckGo"""
    try:
        from duckduckgo_search import DDGS
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=3):
                results.append(f"• {r['title']}: {r['body'][:200]}")
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search error: {e}"


def calculator(expression: str) -> str:
    """Calculate a math expression safely"""
    import math
    safe_chars = set("0123456789+-*/().% ")
    if not all(c in safe_chars for c in expression):
        return "Error: only basic arithmetic allowed"
    try:
        result = eval(expression, {"__builtins__": {}}, {
            "sqrt": math.sqrt, "pi": math.pi, "abs": abs
        })
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"


# ── Tool schemas (what Claude sees) ──────────────────────
TOOL_SCHEMAS = [
    {
        "name": "web_search",
        "description": "Search the web for current information on any topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculator",
        "description": "Calculate any math expression.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "e.g. '15 * 8 / 100'"}
            },
            "required": ["expression"]
        }
    }
]


def run_tool(name: str, inputs: dict) -> str:
    """Run a tool by name and return the result"""
    if name == "web_search":
        return web_search(inputs["query"])
    if name == "calculator":
        return calculator(inputs["expression"])
    return f"Unknown tool: {name}"
