from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chat_logic import generate_response
from memory_store import set_user_personality

app = FastAPI()

# 🔐 Allow frontend (browser) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or use ["http://127.0.0.1:5500"] if you want to be strict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    


# 🧠 In-memory short-term chat
session_chat = {}

@app.post("/chat")
async def chat(req: Request):
    data = await req.json()
    user_id = data["user_id"]
    message = data["message"]

    chat_history = session_chat.get(user_id, [])
    chat_history.append(message)
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]
    session_chat[user_id] = chat_history

    ai_reply = generate_response(user_id, message, chat_history)
    chat_history.append(ai_reply)
    session_chat[user_id] = chat_history

    return {"reply": ai_reply}

@app.post("/set_personality")
async def set_personality(req: Request):
    data = await req.json()
    user_id = data["user_id"]
    mood = data["mood"]
    set_user_personality(user_id, mood)
    return {"message": f"Personality set to {mood}"}

from memory_store import get_user_personality

@app.get("/get_personality/{user_id}")
async def get_personality(user_id: str):
    mood = get_user_personality(user_id)
    return {"mood": mood}

