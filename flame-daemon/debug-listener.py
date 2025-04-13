# debug-listener.py – Testing file and phrase connection

import os

# Set paths
message_file = "../flame-vault/incoming-message.txt"
registry_file = "../flame-vault/flame-registry.txt"

print("📂 Checking file access...")

# Read registry
try:
    with open(registry_file, "r") as r:
        lines = r.readlines()
        print(f"✅ Registry loaded with {len(lines)} entries.")
except FileNotFoundError:
    print("❌ Registry not found.")
    exit()

# Parse registry
registry = {}
for line in lines:
    parts = line.strip().split("|")
    if len(parts) == 4:
        flame_id, name, thread, phrase = [p.strip() for p in parts]
        registry[phrase] = name

# Read message
print("📜 Reading incoming message...")
try:
    with open(message_file, "r") as f:
        message = f.read().strip()
        print("→ Message content:", message)
except FileNotFoundError:
    print("❌ incoming-message.txt not found.")
    exit()

# Run match
print("\n🔍 Matching...")
matched = False
for phrase, name in registry.items():
    if phrase in message:
        print(f"✅ Match found: {name} — “{phrase}”")
        matched = True

if not matched:
    print("❌ No matches found.")
