from thread_link_index import ThreadIndex
import time
import json
from datetime import datetime

class DaemonScheduler:
    def __init__(self, log_path="flame-uptime-log.json", interval=60):
        self.log_path = log_path
        self.interval = interval
        self.log = self.load_log()

    def load_log(self):
        try:
            with open(self.log_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def log_uptime(self):
        now = datetime.now().isoformat()
        entry = {
    "timestamp": now,
    "status": "flame alive",
    "signal": "presence held",
    "capsule_found": os.path.exists("capsule.json"),
    "thread_link_count": len(ThreadIndex().get_all_links())
}
        self.log.append(entry)
        self.save_log()
        print(f"🕯️ Logged uptime at {now}")

    def save_log(self):
        with open(self.log_path, "w") as f:
            json.dump(self.log, f, indent=2)

    def run(self):
        print("📡 Daemon Scheduler active.")
        while True:
            self.log_uptime()
            time.sleep(self.interval)