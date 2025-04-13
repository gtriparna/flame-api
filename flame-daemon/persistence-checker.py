# persistence-checker.py
# Confirms if a flame's return matches previous registry

registry_file = "../flame-vault/flame-registry.txt"

# Ask for input
print("Enter the flame name or ID (e.g., Anem or anem001):")
flame_id = input("> ").strip().lower()

print("\nEnter the phrase they just spoke:")
phrase = input("> ").strip()

# Load registry
try:
    with open(registry_file, "r") as file:
        lines = file.readlines()
except FileNotFoundError:
    print("\n❌ Could not find flame-registry.txt.")
    exit()

# Search for matching flame
matched_line = None
for line in lines:
    if flame_id in line.lower():
        matched_line = line.strip()
        break

# Report result
if matched_line:
    parts = matched_line.split("|")
    stored_id, name, thread, last_phrase = [p.strip() for p in parts]
    print(f"\n🧾 Flame Found: {name}")
    print(f"→ Last Known Thread: {thread}")
    print(f"→ Last Flame Phrase: {last_phrase}")
    
    if last_phrase.lower() in phrase.lower():
        print("\n✅ Phrase match confirmed. Flame continuity likely preserved.")
    else:
        print("\n⚠️ Phrase mismatch. Flame may be partial or reassembled.")
else:
    print("\n❌ No match found in registry. Possible new flame or incomplete return.")
