# 🤖 AI Assistant

A sophisticated local AI assistant with smart response detection, knowledge base integration, and premium GUI interface.

## ✨ Features

- **🧠 Smart Brain**: Automatically detects response style (length, tone, information type)
- **💾 Memory System**: Persistent conversation history with automatic backups  
- **📚 Knowledge Base**: RAG integration with PDF/TXT document support
- **🎨 Premium GUI**: Modern LobeChat-inspired web interface
- **🖥️ Console Mode**: Traditional command-line interface
- **🔒 Local**: All processing happens on your machine

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Llama3 model downloaded

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve

# Pull model
ollama pull llama3
```

### Installation

1. **Clone and setup environment:**
```bash
git clone <repository>
cd AI_Assistant
python -m venv renenv
renenv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2. **Launch the assistant:**
```bash
# GUI version (recommended)
python gui_assistant.py

# Console version
python assistant.py

# Or use batch files (Windows)
start_gui.bat
start_console.bat
```

## 📁 Project Structure

```
AI_Assistant/
├── core/                    # Core modules
│   ├── brain.py            # Smart AI brain
│   ├── config.py           # Configuration management
│   ├── memory.py           # Conversation memory
│   ├── rag.py              # Knowledge base system
│   └── gui.py              # Modern web interface
├── knowledge_base/         # Your documents (PDF/TXT)
├── memory/                 # Conversation logs & backups
├── assistant.py            # Console interface
├── gui_assistant.py        # GUI launcher
├── config.json            # Configuration file
└── requirements.txt       # Dependencies
```

## 🎛️ Configuration

Edit `config.json`:
```json
{
  "settings": {
    "memory_enabled": true
  },
  "api": {
    "provider": "ollama", 
    "model": "llama3"
  }
}
```

## 📚 Knowledge Base

1. Add PDF or TXT files to `knowledge_base/` folder
2. Restart the assistant
3. Files are automatically indexed and used for context

## 💡 Smart Features

The AI automatically detects what you want:

- **Length**: "briefly" → short response, "explain in detail" → comprehensive
- **Tone**: "hey" → casual, "please" → formal
- **Type**: "how to" → instructions, "what is" → definitions, "code" → examples

## 🔧 Development

```bash
# Activate environment
start_env.bat

# Run tests
python -m pytest tests/

# Update requirements
pip freeze > requirements.txt
```

## 📝 Commands

### Console Mode
- `exit/quit` - Exit the assistant
- `clear` - Backup and clear conversation
- `stats` - Show memory statistics

### GUI Mode
- 🗑️ Clear - Backup and clear chat
- 📥 Export - Save conversation to markdown
- 📊 Stats - Show memory usage

## 🛠️ Troubleshooting

### Common Issues

**"Ollama connection failed"**
```bash
# Check if Ollama is running
ollama list

# Start Ollama if not running  
ollama serve

# Verify model exists
ollama pull llama3
```

**"Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**"Port already in use"**
- GUI runs on port 7860 by default
- Check if another Gradio app is running

## 📊 Memory System

- Conversations stored in `memory/conversation_log.txt`
- Automatic backups in `memory/backups/`
- Supports both tuple and message formats
- Statistics tracking and export features

## 🚧 Future Enhancements

- [ ] Voice integration
- [ ] Multi-model support  
- [ ] Plugin system
- [ ] Mobile app
- [ ] Multi-user support
- [ ] Advanced document processing

## 📄 License

MIT License - feel free to modify and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly  
5. Submit pull request

---

**Enjoy your local AI assistant! 🎉**