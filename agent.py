from groq import Groq
from dotenv import load_dotenv
import os
import time
from ddgs import DDGS
load_dotenv()
client=Groq(api_key=os.getenv("groq_api_key"))
def search_web(query):
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=3)]
    return results
messages=[
    {"role":"system","content":"You are my good AI assistant"}
]
print("your AI agent is at your service feel free to ask!Type 'quit' to exit.\n")
while True:
    user_input=input("You:")
    if user_input.lower()=="quit" :
        print("Goodbye dear user!")
        break
    messages.append({"role":"user","content":user_input})


    search_keywords = [
    "latest", "today", "current", "news",
    "price", "who won", "2025", "2026",
    "weather", "score", "recent", "new",
    "what happened", "update"
]
    if any(word in user_input.lower() for word in search_keywords):
     search_results = search_web(user_input)
     search_text = "\n".join([r['body'] for r in search_results])
     messages.append({
        "role": "system",
        "content": f"Here is some web info to help answer:\n{search_text}"
    })
    else:
        pass


    print("Agent is thinking", end="")
    for i in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    reply=response.choices[0].message.content 
    messages.append({"role": "assistant", "content": reply})
    print(f"agent:{reply}\n")