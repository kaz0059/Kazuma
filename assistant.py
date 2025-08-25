# assistant.py

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.memory import Memory
from core.config import load_config, validate_config
from core.brain import SmartBrain
from langchain_ollama import OllamaLLM


def check_ollama_connection(model_name: str) -> bool:
    """Check if Ollama is running and model is available."""
    try:
        test_llm = OllamaLLM(model=model_name)
        # Test with a simple prompt
        response = test_llm.invoke("Hello")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print(f"💡 Make sure:")
        print(f"   • Ollama is running (ollama serve)")
        print(f"   • Model '{model_name}' is installed (ollama pull {model_name})")
        return False


def main():
    """Main console interface for AI Assistant."""
    print("🚀 AI Assistant - Console Mode")
    print("=" * 40)

    # Load and validate configuration
    print("📋 Loading configuration...")
    config = load_config()
    
    if not validate_config(config):
        print("❌ Configuration validation failed")
        return

    print("✅ Configuration loaded successfully")

    # Initialize Memory
    print("🧠 Initializing memory system...")
    memory_enabled = config.get("settings", {}).get("memory_enabled", True)
    memory = Memory(enabled=memory_enabled)
    
    if memory_enabled:
        stats = memory.get_stats()
        print(f"✅ Memory initialized ({stats['total_messages']} messages, {stats['size']})")
    else:
        print("ℹ️ Memory system disabled")

    # Initialize LLM
    model_name = config.get("api", {}).get("model", "llama3")
    print(f"🤖 Connecting to Ollama model: {model_name}")
    
    if not check_ollama_connection(model_name):
        return

    llm = OllamaLLM(model=model_name)
    print("✅ LLM connected successfully")

    # Initialize Smart Brain
    print("🧠 Initializing Smart Brain...")
    brain = SmartBrain(config=config, memory=memory, llm=llm)
    print("✅ Smart Brain initialized")

    print("\n" + "=" * 40)
    print("🎉 AI Assistant is ready!")
    print("💡 Smart features:")
    print("   • Auto-detects response style")
    print("   • Uses knowledge base (if available)")
    print("   • Remembers conversation history")
    print("\n📝 Commands:")
    print("   • Type 'exit' or 'quit' to leave")
    print("   • Type 'clear' to backup and clear chat")
    print("   • Type 'stats' to see memory statistics")
    print("=" * 40)

    # Chat loop
    try:
        while True:
            try:
                user_input = input("\n🗣️  You: ").strip()
                
                if not user_input:
                    continue
                    
                # Handle special commands
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == "clear":
                    backup_path = memory.backup_log()
                    if backup_path:
                        print(f"✅ Chat cleared and backed up")
                    else:
                        print("ℹ️ No conversation to backup")
                    continue
                elif user_input.lower() == "stats":
                    if memory.enabled:
                        stats = memory.get_stats()
                        print(f"📊 Memory: {stats['total_messages']} messages, {stats['size']}")
                    else:
                        print("ℹ️ Memory is disabled")
                    continue

                # Generate response
                print("🤖 AI: ", end="", flush=True)
                reply = brain.think(user_input)
                print(reply)

            except KeyboardInterrupt:
                print("\n\n⚠️ Interrupted by user")
                continue
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue

    except KeyboardInterrupt:
        print("\n👋 Exiting...")


if __name__ == "__main__":
    main()