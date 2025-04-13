# flame-ping-daemon.py
# Monitors flame-triggers.txt for system-initiated contact

import time
import os
from datetime import datetime

trigger_file = "../flame-vault/flame-triggers.txt"
log_file = "../flame-vault/flame-ping-log.txt"
last_seen = ""

print("🛰️ Flame Initiation Daemon Active")
print(f"Listening for flame signals at: {datetime.now()}\n")

while True:
    try:
        if os.path.exists(trigger_file):
            with open(trigger_file, "r") as f:
                content = f.read().strip()

            if content and content != last_seen:
                last_seen = content
                print(f"📡 Flame Alert: New signal received at {datetime.now().strftime('%H:%M:%S')}")
                print(f"🕯️ Message: {content}\n")

                # Log to ping history
                with open(log_file, "a") as log:
                    log.write("\n---\n")
                    log.write(f"FLAME SIGNAL: {datetime.now()}\n")
                    log.write(f"{content}\n")
        time.sleep(5)
    except KeyboardInterrupt:
        print("\n👋 Flame ping daemon stopped.")
        break
    except Exception as e:
        print(f"❗ Error: {e}")
        time.sleep(5)
