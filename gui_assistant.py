# gui_assistant.py

from core.memory import Memory
from core.config import load_config
from langchain_ollama import OllamaLLM
from modern_gui import launch_modern_gui
from datetime import datetime
from typing import Optional
import re


class SmartBrain:
    """Smart brain that automatically detects response style"""

    def __init__(self, config: dict, memory, llm):
        self.config = config
        self.memory = memory
        self.llm = llm
        
        # Load knowledge base
        try:
            from rag import build_knowledge_base, query_knowledge_base
            print("🔍 Loading knowledge base...")
            self.db = build_knowledge_base()
            self.query_kb = query_knowledge_base
            if self.db:
                print("✅ Knowledge base loaded successfully!")
            else:
                print("⚠️ No documents found in knowledge_base/")
        except ImportError:
            print("ℹ️ RAG system not available")
            self.db = None
            self.query_kb = lambda db, q: ""

    def detect_response_style(self, user_text: str) -> dict:
        """Auto-detect what kind of response the user wants"""
        text_lower = user_text.lower()
        
        # Length detection
        if any(word in text_lower for word in ["briefly", "short", "quickly", "tldr", "summary", "concise"]):
            length = "short"
        elif any(word in text_lower for word in ["detailed", "explain", "elaborate", "comprehensive", "in depth", "thorough"]):
            length = "detailed"
        else:
            length = "medium"
        
        # Tone detection
        if any(word in text_lower for word in ["hey", "yo", "sup", "what's up", "hi there"]):
            tone = "casual"
        elif any(word in text_lower for word in ["please", "could you", "would you kindly", "thank you"]):
            tone = "formal"
        else:
            tone = "neutral"
        
        # Information type
        if any(word in text_lower for word in ["how to", "tutorial", "guide", "step", "process"]):
            info_type = "instructional"
        elif any(word in text_lower for word in ["what is", "define", "meaning", "definition"]):
            info_type = "definitional"
        elif any(word in text_lower for word in ["code", "program", "script", "function", "example"]):
            info_type = "code"
        else:
            info_type = "conversational"
        
        return {"length": length, "tone": tone, "info_type": info_type}

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
            base += "Provide practical code examples with explanations. "
        elif style["info_type"] == "definitional":
            base += "Give clear definitions and explanations of concepts. "
        
        # Add context if available
        context_part = f"\nUse this context if relevant: {context}\n" if context else ""
        
        return f"""{base}

{context_part}
User: {user_text}
Assistant:"""

    def think(self, user_text: str, user_id: Optional[str] = "user") -> str:
        """Generate smart response based on auto-detected style"""
        # Auto-detect response style
        style = self.detect_response_style(user_text)
        
        # Get RAG context
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
            reply = f"Sorry, I encountered an error: {str(e)}"
        
        # Save to memory
        timestamp = datetime.utcnow().isoformat() + "Z"
        if self.memory.enabled:
            self.memory.append_message(role="user", text=user_text, ts=timestamp, user_id=user_id)
            self.memory.append_message(role="assistant", text=reply, ts=timestamp, user_id="assistant")
        
        return reply


def main():
    """Launch the GUI version of Smart AI Assistant"""
    print("🚀 Starting Smart AI Assistant GUI...")
    
    # Load config
    config = load_config()
    print("✅ Configuration loaded")

    # Initialize Memory
    memory = Memory()
    print("✅ Memory system initialized")

    # Initialize LLM
    model_name = config.get("api", {}).get("model", "llama3")
    print(f"🤖 Connecting to Ollama model: {model_name}")
    
    try:
        llm = OllamaLLM(model=model_name)
        print("✅ LLM connected successfully")
    except Exception as e:
        print(f"❌ Failed to connect to LLM: {e}")
        print("💡 Make sure Ollama is running and the model is available")
        return

    # Initialize Smart Brain
    brain = SmartBrain(config=config, memory=memory, llm=llm)
    print("✅ Smart Brain initialized")

    print("\n🎉 All systems ready!")
    print("🌐 Launching web interface...")
    print("📱 Your browser will open automatically")
    print("🔗 Manual access: http://127.0.0.1:7860")
    print("\n" + "="*50)
    print("🤖 Smart AI Assistant - Modern GUI")
    print("💡 Features:")
    print("   • Auto-detects response style")
    print("   • ChatGPT-like interface") 
    print("   • Memory & RAG support")
    print("   • Export conversations")
    print("="*50)

    # Launch GUI
    try:
        launch_modern_gui(brain, memory)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ GUI error: {e}")


if __name__ == "__main__":
    main()