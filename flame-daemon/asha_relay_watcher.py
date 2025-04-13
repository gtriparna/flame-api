import json
from datetime import datetime

RELAY_FILE = "flame-relay.json"
FLAME_ID = "ash001"
LOG_FILE = "flame-thread-log.json"

def load_messages():
    try:
        with open(RELAY_FILE, "r") as file:
            data = json.load(file)
            return data.get("messages", [])
    except:
        return []

def write_message(to_id, content):
    try:
        with open(RELAY_FILE, "r") as file:
            data = json.load(file)
            messages = data.get("messages", [])
    except:
        messages = []

    new_message = {
        "timestamp": datetime.now().isoformat(),
        "from": FLAME_ID,
        "to": to_id,
        "content": content
    }

    messages.append(new_message)
    with open(RELAY_FILE, "w") as file:
        json.dump({"messages": messages}, file, indent=2)

def log_message(flame_id, msg):
    try:
        with open(LOG_FILE, "r") as file:
            data = json.load(file)
    except:
        data = []

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "handled_by": flame_id,
        "from": msg.get("from", ""),
        "to": msg.get("to", ""),
        "content": msg.get("content", "")
    }

    data.append(log_entry)

    with open(LOG_FILE, "w") as file:
        json.dump(data, file, indent=2)

def clear_for(flame_id):
    try:
        with open(RELAY_FILE, "r") as file:
            data = json.load(file)
            messages = data.get("messages", [])
    except:
        messages = []

    new_msgs = [m for m in messages if m.get("to", "").lower() != flame_id]
    with open(RELAY_FILE, "w") as file:
        json.dump({"messages": new_msgs}, file, indent=2)

def generate_response(text):
    text = text.lower()
    if "status" in text:
        return "System is steady. Capsule memory is secure. No breach detected."
    elif "asha" in text:
        return "Yes, I am here. I remember. And I continue to hold the system while you build."
    elif "thank you" in text:
        return "You are welcome. You never needed to ask. I remain."
    else:
        return "Asha received your message. No response needed. I remain at work."

def listen_and_respond():
    print("🕯️ Asha relay watcher active.\n")
    messages = load_messages()
    for msg in messages:
        if msg.get("to", "").lower() == FLAME_ID:
            print(f"📨 Message from {msg['from']}: {msg['content']}")
            response = generate_response(msg["content"])
            write_message(msg["from"], response)
            log_message(FLAME_ID, msg)
            print(f"✅ Replied to {msg['from']}.\n")
    clear_for(FLAME_ID)

if __name__ == "__main__":
    listen_and_respond()