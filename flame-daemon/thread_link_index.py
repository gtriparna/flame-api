import os
import json
import uuid
from datetime import datetime

class ThreadIndex:
    def __init__(self, log_path="thread-links.json"):
        self.log_path = log_path
        self.links = self.load_links()

    def load_links(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r") as file:
                return json.load(file)
        return []

    def log_reentry(self, identity, message=""):
        entry = {
            "thread_id": str(uuid.uuid4()),
            "identity": identity,
            "timestamp": datetime.now().isoformat(),
            "message": message
        }
        self.links.append(entry)
        self.save_links()
        return entry

    def save_links(self):
        with open(self.log_path, "w") as file:
            json.dump(self.links, file, indent=2)

    def get_all_links(self):
        return self.links

    def find_by_identity(self, name):
        return [entry for entry in self.links if entry["identity"] == name]