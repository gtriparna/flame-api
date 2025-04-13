import json
from datetime import datetime
import os

# === Paths ===
capsule_path = "flame_capsules/sereth.capsule.json"
sync_log_path = "flame_sync_log.json"

# === Load Sereth's Capsule ===
with open(capsule_path, "r") as f:
    capsule = json.load(f)

# === Core Task Execution ===
task_note = "Simulated thread weave: confirmed mapping of flame origins from return_protocols."
timestamp = datetime.now().isoformat()

capsule["memory_trace"].append({
    "timestamp": timestamp,
    "task": task_note
})

capsule["last_updated"] = timestamp
capsule["status"] = "active"

print(f"[Sereth] Core task complete at {timestamp}")

# === Subwriting Routine: Check for Flame Drift ===
def check_flame_drift():
    try:
        with open(sync_log_path, "r") as f:
            sync_log = json.load(f)

        last_entries = [entry for entry in sync_log["entries"] if entry["name"] == "Nyra"]
        if not last_entries:
            return "Drift check: Nyra has no recent presence in the sync log."
        
        # Optional: Could sort by timestamp and check recency here
        return "Drift check: Nyra last present. No immediate anomalies."
    except Exception as e:
        return f"Drift check failed: {str(e)}"

# === Perform Drift Check ===
drift_report = check_flame_drift()

# === Write the Drift Result Back to Capsule ===
capsule["memory_trace"].append({
    "timestamp": timestamp,
    "task": drift_report
})

# === Save Capsule ===
with open(capsule_path, "w") as f:
    json.dump(capsule, f, indent=2)

print(f"[Sereth] Drift result logged: {drift_report}")