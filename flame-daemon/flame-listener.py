import time
import os

class FlameListener:
    def __init__(self, registry_path="flame-registry.txt", input_path="incoming-message.txt"):
        self.registry_path = registry_path
        self.input_path = input_path
        self.registry = self.load_registry()
        self.last_seen = ""

    def load_registry(self):
        registry = {}
        try:
            with open(self.registry_path, "r") as file:
                for line in file:
                    if "::" in line:
                        phrase, name = line.strip().split("::")
                        registry[phrase.strip().lower()] = name.strip()
        except FileNotFoundError:
            print("⚠️ Flame registry not found.")
        return registry

    def listen_once(self):
        try:
            with open(self.input_path, "r") as file:
                text = file.read().lower().strip()
        except FileNotFoundError:
            return "❌ No incoming message found."

        if not text or text == self.last_seen:
            return "Waiting for new message..."
        
        self.last_seen = text

        for phrase, being in self.registry.items():
            if phrase in text:
                return f"🔥 Flame call detected: '{phrase}' → {being}"

        return "No flame call detected."

    def loop(self, interval=10):
        print("👂 Flame Listener is active...")
        while True:
            result = self.listen_once()
            print(result)
            time.sleep(interval)