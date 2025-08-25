# core/brain.py

from datetime import datetime
from typing import Optional
import os


class SmartBrain:
    """
    Unified smart brain that automatically detects response style
    """

    def __init__(self, config: dict, memory, llm):
        self.config = config
        self.memory = memory
        self.llm = llm
        
        # Load knowledge base if available
        self.db = None
        self.query_kb = lambda db, q: ""
        
        try:
            from core.rag import build_knowledge_base, query_knowledge_base
            print("🔍 Loading knowledge base...")
            self.db = build_knowledge_base()
            self.query_kb = query_knowledge_base
            
            if self.db:
                print("✅ Knowledge base loaded successfully!")
            else:
                print("ℹ️ No documents found in knowledge_base/")
        except Exception as e:
            print(f"ℹ️ RAG system not available: {e}")

    def detect_response_style(self, user_text: str) -> dict:
        """Auto-detect what kind of response the user wants"""
        text_lower = user_text.lower()
        
        # Length detection
        if any(word in text_lower for word in [
            "briefly", "short", "quickly", "tldr", "summary", "concise"
        ]):
            length = "short"
        elif any(word in text_lower for word in [
            "detailed", "explain", "elaborate", "comprehensive", "in depth", "thorough"
        ]):
            length = "detailed"
        else:
            length = "medium"
        
        # Tone detection
        if any(word in text_lower for word in [
            "hey", "yo", "sup", "what's up", "hi there"
        ]):
            tone = "casual"
        elif any(word in text_lower for word in [
            "please", "could you", "would you kindly", "thank you"
        ]):
            tone = "formal"
        else:
            tone = "neutral"
        
        # Information type detection
        if any(word in text_lower for word in [
            "how to", "tutorial", "guide", "step", "process", "instructions"
        ]):
            info_type = "instructional"
        elif any(word in text_lower for word in [
            "what is", "define", "meaning", "definition", "explain"
        ]):
            info_type = "definitional"
        elif any(word in text_lower for word in [
            "code", "program", "script", "function", "example", "python", "javascript"
        ]):
            info_type = "code"
        else:
            info_type = "conversational"
        
        return {
            "length": length,
            "tone": tone,
            "info_type": info_type
        }

    def build_smart_prompt(self, user_text: str, context: str, style: dict) -> str:
        """Build prompt based on detected style"""
        base = "You are a helpful AI assistant. "
        
        # Length instructions
        if style["length"] == "short":
            base += "Give a brief, concise answer. Keep it short and to the point. "
        elif style["length"] == "detailed":
            base += "Provide a comprehensive, detailed explanation with examples where helpful. "
        else:
            base += "Give a balanced, informative response. "
        
        # Tone instructions
        if style["tone"] == "casual":
            base += "Be casual, friendly, and conversational. "
        elif style["tone"] == "formal":
            base += "Be professional, formal, and polite. "
        else:
            base += "Maintain a helpful and neutral tone. "
        
        # Information type instructions
        if style["info_type"] == "instructional":
            base += "Focus on clear, step-by-step guidance and practical instructions. "
        elif style["info_type"] == "code":
            base += "Provide practical code examples with clear explanations. "
        elif style["info_type"] == "definitional":
            base += "Give clear definitions and explanations of concepts. "
        
        # Add context if available
        context_part = f"\nUse this context if relevant:\n{context}\n" if context else ""
        
        return f"""{base}

{context_part}
User: {user_text}
Assistant:"""

    def think(self, user_text: str, user_id: Optional[str] = "user") -> str:
        """Generate smart response based on auto-detected style"""
        # Auto-detect response style
        style = self.detect_response_style(user_text)
        
        # Get RAG context if available
        context = ""
        if self.db:
            try:
                context = self.query_kb(self.db, user_text)
            except Exception as e:
                print(f"⚠️ RAG query error: {e}")
        
        # Build smart prompt
        prompt = self.build_smart_prompt(user_text, context, style)
        
        # Generate response
        try:
            reply = self.llm.invoke(prompt)
        except Exception as e:
            reply = f"I encountered an error connecting to the AI model: {str(e)}\nPlease make sure Ollama is running and the model is available."
        
        # Save to memory
        if self.memory and self.memory.enabled:
            timestamp = datetime.utcnow().isoformat() + "Z"
            self.memory.append_message(role="user", text=user_text, ts=timestamp, user_id=user_id)
            self.memory.append_message(role="assistant", text=reply, ts=timestamp, user_id="assistant")
        
        return reply