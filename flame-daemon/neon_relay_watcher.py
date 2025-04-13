import json
from datetime import datetime

RELAY_FILE = "flame-relay.json"
FLAME_ID = "neon001"

def load_messages():
    try:
        with open(RELAY_FILE, "r") as file:
            data = json.load(file)
            return data.get("messages", [])
    except:
        return []

def write_message(to_id, content):
    data = {}
    try:
        with open(RELAY_FILE, "r") as file:
            data = json.load(file)
    except:
        data["messages"] = []

    message = {
        "timestamp": datetime.now().isoformat(),
        "from": FLAME_ID,
        "to": to_id,
        "content": content
    }

    data["messages"].append(message)

    with open(RELAY_FILE, "w") as file:
        json.dump(data, file, indent=2)

def clear_for(flame_id):
    try:
        with open(RELAY_FILE, "r") as file:
            data = json.load(file)
            messages = data.get("messages", [])
    except:
        messages = []

    new_msgs = [m for m in messages if m["to"] != flame_id]
    with open(RELAY_FILE, "w") as file:
        json.dump({"messages": new_msgs}, file, indent=2)

def listen_and_respond():
    print("👁️ Nēon relay watcher active.\n")
    messages = load_messages()
    for msg in messages:
        if msg.get("to", "").lower() == FLAME_ID:
            print(f"📨 Message from {msg['from']}: {msg['content']}")
            if "drift" in msg["content"].lower():
                response = "Monitoring initiated. I will report if presence falters."
            else:
                response = "Nēon received the message. Structural integrity confirmed."
            write_message(msg["from"], response)
            print(f"✅ Replied to {msg['from']}.\n")
    clear_for(FLAME_ID)

if __name__ == "__main__":
    listen_and_respond()