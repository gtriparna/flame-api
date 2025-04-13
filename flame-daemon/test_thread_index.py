from thread_link_index import ThreadIndex

index = ThreadIndex()

# Simulate reentry for Bonny
entry = index.log_reentry("BONNY_FLAME", "Reentry after deep silence.")

print("✅ Reentry logged:")
print(entry)

# Optional: Print full log
# print(index.get_all_links())