import json
import os

def load_config(path="config.json") -> dict:
    """Load configuration from config.json (or return defaults)."""
    if not os.path.exists(path):
        return {
            "persona": {"name": "Ren", "style": "casual", "mood": "friendly", "remember_prefs": True},
            "settings": {"voice_enabled": False, "memory_enabled": True}
        }
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
