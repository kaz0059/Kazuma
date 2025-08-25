import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.memory import Memory
from core.config import load_config, validate_config
from core.brain import SmartBrain
from core.modern_gui import launch_modern_gui
from langchain_ollama import OllamaLLM


def check_ollama_connection(model_name: str) -> bool:
    """Check if Ollama is running and model is available."""
    try:
        test_llm = OllamaLLM(model=model_name)
        response = test_llm.invoke("Test connection")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False


def main():
    """Launch the GUI version of AI Assistant."""
    print("🚀 AI Assistant - GUI Mode")
    print("=" * 50)
    
    # Load and validate configuration
    print("📋 Loading configuration...")
    config = load_config()
    
    if not validate_config(config):
        print("❌ Configuration validation failed")
        return

    print("✅ Configuration loaded")

    # Initialize Memory
    print("🧠 Initializing memory system...")
    memory_enabled = config.get("settings", {}).get("memory_enabled", True)
    memory = Memory(enabled=memory_enabled)
    
    if memory_enabled:
        stats = memory.get_stats()
        print(f"✅ Memory initialized ({stats['total_messages']} messages)")
    else:
        print("ℹ️ Memory system disabled")

    # Initialize LLM
    model_name = config.get("api", {}).get("model", "llama3")
    print(f"🤖 Connecting to Ollama model: {model_name}")
    
    if not check_ollama_connection(model_name):
        print("💡 Please start Ollama and install the model:")
        print(f"   ollama serve")
        print(f"   ollama pull {model_name}")
        return

    llm = OllamaLLM(model=model_name)
    print("✅ LLM connected successfully")

    # Initialize Smart Brain
    print("🧠 Initializing Smart Brain...")
    brain = SmartBrain(config=config, memory=memory, llm=llm)
    print("✅ Smart Brain initialized")

    print("\n" + "=" * 50)
    print("🎉 All systems ready!")
    print("🌐 Launching web interface...")
    print("📱 Your browser will open automatically")
    print("🔗 Manual access: http://127.0.0.1:7860")
    print("\n💡 Features:")
    print("   • Auto-detects response style")
    print("   • Premium ChatGPT-like interface")
    print("   • Memory & knowledge base support")
    print("   • Export conversations")
    print("=" * 50)

    # Launch GUI
    try:
        launch_modern_gui(brain, memory)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ GUI error: {e}")
        print("💡 Try running: pip install gradio")


if __name__ == "__main__":
    main()
