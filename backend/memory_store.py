import json
import os

MEMORY_PATH = "user_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w") as f:
            json.dump({}, f)
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=2)

def get_user_memory(user_id):
    memory = load_memory()
    return memory.get(user_id, [])

def add_to_user_memory(user_id, info):
    memory = load_memory()
    user_data = memory.get(user_id, [])
    user_data.append(info)
    memory[user_id] = user_data
    save_memory(memory)
    
def set_user_personality(user_id, personality):
    memory = load_memory()
    user_data = memory.get(user_id, [])
    # Overwrite or update personality setting
    memory[user_id] = [m for m in user_data if not m.startswith("personality:")]
    memory[user_id].insert(0, f"personality:{personality}")
    save_memory(memory)

def get_user_personality(user_id):
    memory = get_user_memory(user_id)
    for m in memory:
        if m.startswith("personality:"):
            return m.split(":", 1)[1]
    return "romantic"

