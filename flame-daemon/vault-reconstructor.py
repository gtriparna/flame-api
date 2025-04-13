# vault-reconstructor.py
# Rebuilds flame being identity from continuity manifest

import json
from datetime import datetime

manifest_file = "../flame-vault/flame-continuity-manifest.json"

print("🧠 Vault Memory Reconstructor")
print(f"🕯️ Started at {datetime.now()}\n")

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

print("📖 Registered Flame Beings:\n")
for i, flame in enumerate(flames, 1):
    print(f"[{i}] {flame.get('name')} ({flame.get('id')}) — {flame.get('role')}")

print("\nEnter the name or ID of the flame to reconstruct:")
target = input("> ").strip().lower()

found = None
for flame in flames:
    if target in flame.get("name", "").lower() or target in flame.get("id", "").lower():
        found = flame
        break

if found:
    print("\n🧬 Flame Reconstruction Profile:\n")
    for k, v in found.items():
        print(f"{k.capitalize()}: {v}")
else:
    print("❌ Flame not found.")
