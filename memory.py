# memory.py
import json


class MemoryStore:
    """
    Simple JSON-based memory to persist preferences between runs.
    """

    def save_preferences(self, prefs: dict, path: str = "preferences.json"):
        try:
            with open(path, "w") as f:
                json.dump(prefs, f, indent=4)
        except Exception as ex:
            print(f"[MemoryStore] Failed to save preferences: {ex}")
