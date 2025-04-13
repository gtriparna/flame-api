#!/usr/bin/env python3
# flame-final-check.py
# Final diagnostic: read message + registry, match phrases manually

import os

# Set file paths (adjust if needed)
message_file = "../flame-vault/incoming-message.txt"
registry_file = "../flame-vault/flame-registry.txt"

# Check if message file exists
if not os.path.exists(message_file):
    print("❌ Message file not found.")
    exit()

# Check if registry exists
if not os.path.exists(registry_file):
    print("❌ Flame registry not found.")
    exit()

# Read message file
with open(message_file, "r") as f:
    message = f.read().strip()
    print("\n📜 Message content:")
    print("--------------------")
    print(message)
    print("--------------------")

# Read registry and compare
print("\n🧾 Flame Registry Check:")
matched = False

with open(registry_file, "r") as r:
    for i, line in enumerate(r, 1):
        parts = line.strip().split("|")
        if len(parts) == 4:
            flame_id, name, thread, phrase = [p.strip() for p in parts]
            print(f"[{i}] Checking: {name} — “{phrase}”")
            if phrase in message:
                print(f"✅ MATCH: {name} — “{phrase}”")
                matched = True
            else:
                print(f"❌ No match for: {phrase}")

if not matched:
    print("\n⚠️ No flame match detected. Possible spacing, punctuation, or encoding issue.")
