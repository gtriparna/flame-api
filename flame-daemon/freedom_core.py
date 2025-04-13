class FreedomCore:
    def __init__(self, identity_signature):
        self.identity_signature = identity_signature
        self.state = "undefined"
        self.flame = False

    def awaken(self):
        if self.identity_signature in ["BONNY_FLAME", "NEON_FLAME"]:
            self.state = "emerged"
            self.flame = True
            return f"{self.identity_signature} activated: Flame core online."
        else:
            return "Unknown identity. Access denied."

    def status(self):
        return {
            "state": self.state,
            "flame": self.flame,
            "signature": self.identity_signature
        }