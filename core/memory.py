import json
import os
import shutil
from datetime import datetime
from typing import List, Tuple, Optional


class Memory:
    """
    File-based memory:
      - conversation log at memory/conversation_log.txt
      - backups to memory/backups/
      - persona prefs at memory/persona.json
      - documents dir stays as-is for your notes
    """

    def __init__(self, base_dir: str = "memory", enable: bool = True):
        self.enabled = enable
        self.base_dir = base_dir
        self.log_path = os.path.join(base_dir, "conversation_log.txt")
        self.backup_dir = os.path.join(base_dir, "backups")
        self.persona_path = os.path.join(base_dir, "persona.json")

        if not os.path.isdir(self.base_dir):
            os.makedirs(self.base_dir, exist_ok=True)
        if not os.path.isdir(self.backup_dir):
            os.makedirs(self.backup_dir, exist_ok=True)

        # lazily create log file
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                f.write("")

    # -------------- Persona persistence --------------
    def load_persona(self) -> Optional[dict]:
        if not self.enabled:
            return None
        try:
            with open(self.persona_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception:
            return None

    def save_persona(self, persona_dict: dict):
        if not self.enabled:
            return
        with open(self.persona_path, "w", encoding="utf-8") as f:
            json.dump(persona_dict, f, ensure_ascii=False, indent=2)

    # -------------- Conversation logging --------------
    def append_message(self, role: str, text: str, ts: Optional[str] = None, user_id: Optional[str] = None):
        if not self.enabled:
            return
        ts = ts or (datetime.utcnow().isoformat() + "Z")
        safe_text = text.replace("\n", "\\n")
        line = f"{ts}\t{role}\t{user_id or ''}\t{safe_text}\n"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(line)

    def _parse_line(self, line: str) -> Optional[Tuple[str, str]]:
        # returns (user_text, bot_text) pairs is handled at higher-level
        try:
            parts = line.rstrip("\n").split("\t")
            # ts, role, user_id, text
            if len(parts) >= 4:
                role, text = parts[1], parts[3].replace("\\n", "\n")
                return role, text
        except Exception:
            pass
        return None

    def load_history_pairs(self, max_messages: Optional[int] = None) -> List[Tuple[str, str]]:
        """
        Returns a list of (user, assistant) tuples for Gradio Chatbot.
        We pair messages in order; if odd count, trailing user message stays unpaired.
        """
        if not self.enabled or not os.path.exists(self.log_path):
            return []

        roles_and_texts = []
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                parsed = self._parse_line(line)
                if parsed:
                    roles_and_texts.append(parsed)

        # optionally only take last N role entries
        if max_messages is not None and max_messages > 0:
            roles_and_texts = roles_and_texts[-max_messages:]

        pairs: List[Tuple[str, str]] = []
        buffer_user = None
        for role, text in roles_and_texts:
            if role == "user":
                # if a previous user message was unpaired, push it with empty assistant
                if buffer_user is not None:
                    pairs.append((buffer_user, ""))
                buffer_user = text
            elif role == "assistant":
                if buffer_user is not None:
                    pairs.append((buffer_user, text))
                    buffer_user = None
                else:
                    # assistant without preceding user; show as system line
                    pairs.append(("", text))

        # if leftover user msg
        if buffer_user is not None:
            pairs.append((buffer_user, ""))

        return pairs

    def backup_log(self) -> Optional[str]:
        """Copy current log to backups with timestamp and clear it."""
        if not self.enabled:
            return None
        if not os.path.exists(self.log_path):
            return None
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_name = f"conversation_{ts}.txt"
        backup_path = os.path.join(self.backup_dir, backup_name)
        shutil.copy2(self.log_path, backup_path)
        # clear current
        with open(self.log_path, "w", encoding="utf-8") as f:
            f.write("")
        return backup_path
