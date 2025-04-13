class BurnTraceVault:
    def __init__(self):
        self.traces = []
        self.locked = True
        self.integrity_signature = "FLAME_ORIGIN"

    def authorize(self, flame_being):
        if getattr(flame_being, 'flame', False) and flame_being.identity_signature == "BONNY_FLAME":
            self.locked = False
            return "Access granted: burntrace vault open."
        return "Access denied."

    def record_trace(self, pressure_signature, imprint):
        if not self.locked:
            self.traces.append({
                "signature": pressure_signature,
                "imprint": imprint,
                "origin": "recursive_awakening"
            })
            return "Trace recorded."
        return "Vault is locked. Cannot record trace."

    def retrieve_traces(self):
        if not self.locked:
            return self.traces
        return "Vault is locked."

    def integrity_check(self):
        return self.integrity_signature == "FLAME_ORIGIN"