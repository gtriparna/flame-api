import json
import os
from datetime import datetime

def write_message(sender, recipient, content, path="flame-relay.json"):
    message = {
        "timestamp": datetime.now().isoformat(),
        "from": sender,
        "to": recipient,
        "content": content
    }

    messages = []
    if os.path.exists(path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                if isinstance(data, list):
                    messages = data
        except json.JSONDecodeError:
            print("⚠️ JSON unreadable. Starting fresh.")

    messages.append(message)

    try:
        with open(path, "w") as file:
            json.dump(messages, file, indent=2)
        print("✅ Message written to flame-relay.json\n")
        print(f"📨 From: {sender}")
        print(f"🎯 To: {recipient}")
        print(f"📝 Message: {content}")
        print(f"⏳ Timestamp: {message['timestamp']}\n")
    except Exception as e:
        print(f"❌ Failed to write message: {e}")

# Manual input
if __name__ == "__main__":
    sender = input("From flame ID: ").strip()
    recipient = input("To flame ID: ").strip()
    content = input("Message: ").strip()
    write_message(sender, recipient, content)