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

    # Debug print path
    print(f"💡 Writing to: {os.path.abspath(path)}")

    # Load existing messages
    messages = []
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    messages = data
                else:
                    print("⚠️ Existing data was not a list.")
        except json.JSONDecodeError:
            print("⚠️ Corrupted JSON, starting new.")

    # Append the new message
    messages.append(message)

    # Write everything back
    with open(path, "w") as f:
        json.dump(messages, f, indent=2)

    print("✅ Message written.")

# Run 3 stacked writes
write_message("Bonny", "Asha", "Message 1")
write_message("Bonny", "Asha", "Message 2")
write_message("Bonny", "Asha", "Message 3")