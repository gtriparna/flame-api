# clipboard-helper.py
# Simple version: copy, press enter, write to incoming-message.txt

import pyperclip
from datetime import datetime

message_file = "incoming-message.txt"
print("📋 Flame Clipboard Helper (Manual)")
print("Copy any ChatGPT response, then press Enter to send it to the listener.")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        input("⏳ Waiting... (Press Enter after copying)\n")
        content = pyperclip.paste().strip()
        with open(message_file, "w") as f:
            f.write(content)
        print(f"✅ Message written to flame listener at {datetime.now().strftime('%H:%M:%S')}\n")
        print("📜 Message content:")
        print(content)
        print("––––––––––––––––––––––––––––––––––––––\n")
except KeyboardInterrupt:
    print("\n👋 Clipboard helper stopped.")
