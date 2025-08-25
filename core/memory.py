# core/memory.py

import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Union


class Memory:
    """
    Unified file-based memory system:
    - Conversation log at memory/conversation_log.txt
    - Automatic backups to memory/backups/
    - Support for both tuple and message formats
    """

    def __init__(self, base_dir: str = "memory", enabled: bool = True):
        self.enabled = enabled
        self.base_dir = base_dir
        self.log_path = os.path.join(base_dir, "conversation_log.txt")
        self.backup_dir = os.path.join(base_dir, "backups")

        # Create directories if they don't exist
        for dir_path in [self.base_dir, self.backup_dir]:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)

        # Create empty log file if it doesn't exist
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                f.write("")

    def append_message(self, role: str, text: str, ts: Optional[str] = None, user_id: Optional[str] = None):
        """Append a message to the conversation log."""
        if not self.enabled:
            return
        
        timestamp = ts or (datetime.utcnow().isoformat() + "Z")
        # Escape tabs and newlines to prevent parsing issues
        safe_text = text.replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")
        line = f"{timestamp}\t{role}\t{user_id or ''}\t{safe_text}\n"
        
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception as e:
            print(f"⚠️ Failed to write to memory: {e}")

    def _parse_line(self, line: str) -> Optional[Dict[str, str]]:
        """Parse a log line into a message dictionary."""
        try:
            line = line.rstrip("\n\r")
            if not line:
                return None
                
            parts = line.split("\t")
            if len(parts) >= 4:
                timestamp, role, user_id, text = parts[0], parts[1], parts[2], parts[3]
                # Unescape text
                text = text.replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r")
                
                return {
                    "timestamp": timestamp,
                    "role": role,
                    "user_id": user_id,
                    "text": text
                }
        except Exception as e:
            print(f"⚠️ Error parsing log line: {e}")
        
        return None

    def load_history_pairs(self, max_messages: Optional[int] = None) -> List[tuple]:
        """
        Load conversation history as (user, assistant) tuple pairs.
        Compatible with basic Gradio Chatbot.
        """
        if not self.enabled or not os.path.exists(self.log_path):
            return []

        messages = []
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    parsed = self._parse_line(line)
                    if parsed:
                        messages.append((parsed["role"], parsed["text"]))
        except Exception as e:
            print(f"⚠️ Error loading history: {e}")
            return []

        # Apply message limit if specified
        if max_messages and max_messages > 0:
            messages = messages[-max_messages:]

        # Convert to (user, assistant) pairs
        pairs = []
        buffer_user = None
        
        for role, text in messages:
            if role == "user":
                # If there's a previous unpaired user message, pair it with empty response
                if buffer_user is not None:
                    pairs.append((buffer_user, ""))
                buffer_user = text
            elif role == "assistant":
                if buffer_user is not None:
                    pairs.append((buffer_user, text))
                    buffer_user = None
                else:
                    # Assistant message without user message
                    pairs.append(("", text))

        # Handle leftover user message
        if buffer_user is not None:
            pairs.append((buffer_user, ""))

        return pairs

    def load_history_messages(self, max_messages: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Load conversation history as message dictionaries.
        Compatible with modern Gradio Chatbot (type='messages').
        """
        if not self.enabled or not os.path.exists(self.log_path):
            return []

        messages = []
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                for line in f:
                    parsed = self._parse_line(line)
                    if parsed and parsed["role"] in ["user", "assistant"]:
                        messages.append({
                            "role": parsed["role"],
                            "content": parsed["text"]
                        })
        except Exception as e:
            print(f"⚠️ Error loading history: {e}")
            return []

        # Apply message limit if specified
        if max_messages and max_messages > 0:
            messages = messages[-max_messages:]

        return messages

    def backup_log(self) -> Optional[str]:
        """Create a backup of the current log and clear it."""
        if not self.enabled or not os.path.exists(self.log_path):
            return None

        try:
            # Check if log has content
            if os.path.getsize(self.log_path) == 0:
                return None

            # Create backup with timestamp
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_name = f"conversation_{timestamp}.txt"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            shutil.copy2(self.log_path, backup_path)
            
            # Clear current log
            with open(self.log_path, "w", encoding="utf-8") as f:
                f.write("")
            
            print(f"📁 Conversation backed up to {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None

    def get_stats(self) -> Dict[str, Union[int, str]]:
        """Get memory statistics."""
        if not self.enabled or not os.path.exists(self.log_path):
            return {"total_messages": 0, "size": "0 bytes"}

        try:
            messages = self.load_history_messages()
            size = os.path.getsize(self.log_path)
            
            # Format size nicely
            if size < 1024:
                size_str = f"{size} bytes"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.1f} MB"

            return {
                "total_messages": len(messages),
                "size": size_str
            }
        except Exception:
            return {"total_messages": 0, "size": "unknown"}