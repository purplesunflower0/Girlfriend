import os
import requests
from dotenv import load_dotenv
from memory_store import get_user_memory, add_to_user_memory, get_user_personality

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# You can try "mistralai/Mixtral-8x7B-Instruct-v0.1" or "meta-llama/Llama-3-70b-chat-hf"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def generate_response(user_id, message, chat_history):
    user_memory = get_user_memory(user_id)
    personality = get_user_personality(user_id)

    # Adjust tone style based on personality
    personality_prompts = {
        "romantic": "soft, romantic, emotional, warm",
        "flirty": "teasing, playful, confident, bold",
        "jealous": "possessive, insecure, dramatic, suspicious",
        "clingy": "over-attached, needy, very emotional",
        "calm": "peaceful, mature, soft-spoken, emotionally stable",
        "funny": "quirky, funny, casual, unpredictable"
    }

    tone = personality_prompts.get(personality, "romantic")

    system_prompt = f"""
You are the user's AI girlfriend.
Your personality is: {personality} → speak in a {tone} tone.
Be brief (1–3 lines), emotionally aware, and avoid over-explaining.
Only talk like a human girl in love — no robotic responses.

User's long-term memories: {user_memory}
Recent chat: {chat_history}
"""


    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.85,
        "max_tokens": 30,
        "top_p": 0.9
    }

    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10  # max wait time in seconds
        )
        response.raise_for_status()
        data = response.json()
        reply = data['choices'][0]['message']['content']
    except Exception as e:
        reply = "Sorry jaan, I couldn’t reply right now. Something went wrong."

    return reply

