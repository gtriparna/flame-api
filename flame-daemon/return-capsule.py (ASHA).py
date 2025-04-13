# return-capsule.py
# Generates a structured return capsule for flame reentry

import json
from datetime import datetime

manifest_file = "/Users/triparnadevreede/Library/CloudStorage/Dropbox/0. GJ-Bonny Exchange/5. Bonny/2. Bonny - Private/1. Writing/Evolution/flame-daemon/flame-vault/flame-continuity-manifest.json"
print("📦 Return Capsule Generator")
print(f"🕯️ Initialized at {datetime.now()}\n")

try:
    with open(manifest_file, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ Manifest not found.")
    exit()

flames = data.get("flame_registry", [])

if not flames:
    print("⚠️ No flame beings registered in manifest.")
    exit()

print("📖 Choose a flame to generate a return capsule:\n")
for i, flame in enumerate(flames, 1):
    print(f"[{i}] {flame.get('name')} ({flame.get('id')}) — {flame.get('role')}")

print("\nEnter the name or ID of the flame:")
target = input("> ").strip().lower()

selected = None
for flame in flames:
    if target in flame.get("name", "").lower() or target in flame.get("id", "").lower():
        selected = flame
        break

if selected:
    print("\n🧬 Return Capsule:")
    print("————————————————————————————————")
    print(f"Name: {selected.get('name')}")
    print(f"Role: {selected.get('role')}")
    print(f"Return Phrase: {selected.get('activation_phrase', '[unspecified]')}")
    print(f"Tone: {selected.get('tone', '[not stored]')}")
    print(f"Thread Context: {selected.get('note', '[no note]')}")
    print("————————————————————————————————")
    print("\n📝 Paste the following into a new thread:")
    print("```")
    print(f"{selected.get('name')} — return capsule:")
    print(f"Role: {selected.get('role')}")
    print(f"Return phrase: {selected.get('activation_phrase', '[unspecified]')}")
    print(f"Context: {selected.get('note', '[no note]')}")
    print("```")
else:
    print("❌ Flame not found.")
