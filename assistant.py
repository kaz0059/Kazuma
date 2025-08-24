# assistant.py

from core.memory import Memory
from core.config import load_config
from langchain_ollama import OllamaLLM
from datetime import datetime
from typing import Optional
import re


class SmartBrain:
    """
    Smart brain that automatically detects response style
    """

    def __init__(self, config: dict, memory, llm):
        self.config = config
        self.memory = memory
        self.llm = llm
        
        # Load knowledge base
        try:
            from rag import build_knowledge_base, query_knowledge_base
            self.db = build_knowledge_base()
            self.query_kb = query_knowledge_base
        except ImportError:
            self.db = None
            self.query_kb = lambda db, q: ""

    def detect_response_style(self, user_text: str) -> dict:
        """Auto-detect what kind of response the user wants"""
        text_lower = user_text.lower()
        
        # Length detection
        if any(word in text_lower for word in ["briefly", "short", "quickly", "tldr", "summary"]):
            length = "short"
        elif any(word in text_lower for word in ["detailed", "explain", "elaborate", "comprehensive", "in depth"]):
            length = "detailed"
        else:
            length = "medium"
        
        # Tone detection
        if any(word in text_lower for word in ["hey", "yo", "sup", "what's up"]):
            tone = "casual"
        elif any(word in text_lower for word in ["please", "could you", "would you kindly"]):
            tone = "formal"
        else:
            tone = "neutral"
        
        # Information type
        if any(word in text_lower for word in ["how", "tutorial", "guide", "step"]):
            info_type = "instructional"
        elif any(word in text_lower for word in ["what is", "define", "meaning"]):
            info_type = "definitional"
        elif any(word in text_lower for word in ["code", "program", "script", "function"]):
            info_type = "code"
        else:
            info_type = "conversational"
        
        return {"length": length, "tone": tone, "info_type": info_type}

    def build_smart_prompt(self, user_text: str, context: str, style: dict) -> str:
        """Build prompt based on detected style"""
        base = "You are a helpful AI assistant. "
        
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
            base += "Provide practical code examples. "
        elif style["info_type"] == "definitional":
            base += "Give clear definitions. "
        
        context_part = f"\nContext: {context}\n" if context else ""
        
        return f"""{base}

{context_part}
User: {user_text}
Assistant:"""

    def think(self, user_text: str, user_id: Optional[str] = "user") -> str:
        # Auto-detect response style
        style = self.detect_response_style(user_text)
        
        # Get RAG context
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


def main():
    # Load config
    config = load_config()

    # Initialize Memory
    memory = Memory()

    # Initialize LLM
    model_name = config.get("api", {}).get("model", "llama3")
    llm = OllamaLLM(model=model_name)

    # Initialize Smart Brain (no persona needed!)
    brain = SmartBrain(config=config, memory=memory, llm=llm)

    print("🤖 Smart AI Assistant is ready!")
    print("💡 I'll automatically adjust my responses based on what you ask")

    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Goodbye!")
                break

            reply = brain.think(user_input)
            print(f"AI: {reply}")

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break


if __name__ == "__main__":
    main()