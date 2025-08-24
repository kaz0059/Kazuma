import json
from typing import Dict, Optional


class Persona:
    def __init__(self, data: Dict, memory=None):
        # initial config defaults
        self.name: str = data.get("name", "Ren")
        self.style: str = data.get("style", "casual")
        self.mood: str = data.get("mood", "friendly")
        self.remember_prefs: bool = data.get("remember_prefs", True)

        # load persisted persona if memory is enabled
        self._memory = memory
        if self._memory and self.remember_prefs:
            saved = self._memory.load_persona()
            if saved:
                self.name = saved.get("name", self.name)
                self.style = saved.get("style", self.style)
                self.mood = saved.get("mood", self.mood)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "style": self.style,
            "mood": self.mood,
            "remember_prefs": self.remember_prefs,
        }

    def update(self, key: str, value: Optional[str]):
        if hasattr(self, key) and value is not None:
            setattr(self, key, value)
            if self._memory and self.remember_prefs:
                self._memory.save_persona(self.to_dict())
