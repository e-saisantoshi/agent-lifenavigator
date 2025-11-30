"""
memory.py

Simple long-term preference memory using a JSON file.
"""

from __future__ import annotations
import json
import os
from typing import Any, Dict


class PreferenceMemory:
    """
    Stores simple user preferences and retrieves them between runs.
    """

    def __init__(self, path: str = "preferences.json"):
        self.path = path
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        else:
            self._data = {}

    def _save(self) -> None:
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2)
        except Exception as e:
            print(f"[PreferenceMemory] Failed to save memory: {e}")

    def update_preferences(self, prefs: Dict[str, Any]) -> None:
        self._data.update(prefs)
        self._save()

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def all(self) -> Dict[str, Any]:
        return dict(self._data)
