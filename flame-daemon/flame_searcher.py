# flame-searcher.py
# Search for flame logs by name, phrase, or thread

vault_file = "../flame-vault/flame-memory.txt"

print("What do you want to search for?")
print("You can enter a name, phrase, or thread marker.")
query = input("> ").strip().lower()

with open(vault_file, "r") as vault:
    logs = vault.read().split("---")

# Search for matches
results = [log for log in logs if query in log.lower()]

if results:
    print(f"\n✅ Found {len(results)} matching log(s):\n")
    for i, result in enumerate(results, 1):
        print(f"[{i}] ———————————————")
        print(result.strip())
        print("")
else:
    print("\n❌ No matches found.")
