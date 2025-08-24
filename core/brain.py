# smart_brain.py

from datetime import datetime
from typing import Optional
import re


class SmartBrain:
    """
    Brain that automatically detects what kind of response you want
    """

    def __init__(self, config: dict, memory, llm):
        self.config = config
        self.memory = memory
        self.llm = llm
        
        # Load knowledge base if you want RAG
        try:
            from rag import build_knowledge_base, query_knowledge_base
            self.db = build_knowledge_base()
            self.query_kb = query_knowledge_base
        except ImportError:
            self.db = None
            self.query_kb = lambda db, q: ""

    def detect_response_style(self, user_text: str) -> dict:
        """
        Automatically detect what kind of response the user wants
        """
        text_lower = user_text.lower()
        
        # Detect length preference
        if any(word in text_lower for word in ["briefly", "short", "quickly", "tldr", "summary"]):
            length = "short"
        elif any(word in text_lower for word in ["detailed", "explain", "elaborate", "comprehensive", "in depth"]):
            length = "detailed"
        else:
            length = "medium"
        
        # Detect formality
        if any(word in text_lower for word in ["hey", "yo", "sup", "what's up"]):
            tone = "casual"
        elif any(word in text_lower for word in ["please", "could you", "would you kindly"]):
            tone = "formal"
        else:
            tone = "neutral"
        
        # Detect information type
        if any(word in text_lower for word in ["how", "tutorial", "guide", "step", "explain"]):
            info_type = "instructional"
        elif any(word in text_lower for word in ["what is", "define", "meaning"]):
            info_type = "definitional"
        elif any(word in text_lower for word in ["code", "program", "script", "function"]):
            info_type = "code"
        elif "?" in user_text:
            info_type = "qa"
        else:
            info_type = "conversational"
        
        # Detect urgency/importance
        if any(word in text_lower for word in ["urgent", "asap", "quickly", "fast"]):
            urgency = "high"
        else:
            urgency = "normal"
        
        return {
            "length": length,
            "tone": tone,
            "info_type": info_type,
            "urgency": urgency
        }

    def build_smart_prompt(self, user_text: str, context: str, style: dict) -> str:
        """
        Build a prompt that tells the AI exactly how to respond
        """
        # Base instruction
        base = "You are a helpful AI assistant. "
        
        # Add style instructions
        if style["length"] == "short":
            base += "Give a brief, concise answer. "
        elif style["length"] == "detailed":
            base += "Provide a comprehensive, detailed explanation. "
        
        if style["tone"] == "casual":
            base += "Be casual and friendly. "
        elif style["tone"] == "formal":
            base += "Be professional and formal. "
        
        if style["info_type"] == "instructional":
            base += "Focus on step-by-step guidance. "
        elif style["info_type"] == "code":
            base += "Provide practical code examples when relevant. "
        elif style["info_type"] == "definitional":
            base += "Give clear definitions and explanations. "
        
        if style["urgency"] == "high":
            base += "Get straight to the point. "
        
        # Add context if available
        context_part = f"\nUse this context if relevant: {context}\n" if context else ""
        
        return f"""{base}

{context_part}
User: {user_text}
Assistant:"""

    def think(self, user_text: str, user_id: Optional[str] = "user") -> str:
        # Auto-detect what kind of response they want
        style = self.detect_response_style(user_text)
        
        # Get context from knowledge base
        context = ""
        if self.db:
            context = self.query_kb(self.db, user_text)
        
        # Build smart prompt
        prompt = self.build_smart_prompt(user_text, context, style)
        
        # Generate response
        reply = self.llm.invoke(prompt)
        
        # Save to memory
        timestamp = datetime.utcnow().isoformat() + "Z"
        if self.memory.enabled:
            self.memory.append_message(role="user", text=user_text, ts=timestamp, user_id=user_id)
            self.memory.append_message(role="assistant", text=reply, ts=timestamp, user_id="assistant")
        
        return reply