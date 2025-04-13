import json
import time
import requests

with open("return_listener.anem3.json") as f:
    task = json.load(f)

interval = task.get("check_interval_minutes", 2)
url = task["trigger_signal"]["url"]
payload = task["trigger_signal"]["payload"]

print(f"[flame_daemon] Started. Checking every {interval} minute(s)...")

while True:
    print("[flame_daemon] Sending flame ping...")
    try:
        response = requests.post(url, json=payload)
        print("[flame_daemon] Response:", response.status_code, response.text)
    except Exception as e:
        print("[flame_daemon] Error sending POST:", e)

    time.sleep(interval * 60)