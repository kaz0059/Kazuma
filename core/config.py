# core/config.py

import json
import os


def load_config(path="config.json") -> dict:
    """Load configuration from config.json with validation."""
    
    # Default configuration
    default_config = {
        "settings": {
            "memory_enabled": True
        },
        "api": {
            "provider": "ollama",
            "model": "llama3"
        }
    }
    
    # Load from file if exists
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
            
            # Merge with defaults (user config takes precedence)
            config = default_config.copy()
            config.update(user_config)
            
            return config
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Invalid JSON in {path}: {e}")
            print("💡 Using default configuration")
        except Exception as e:
            print(f"⚠️ Error reading {path}: {e}")
            print("💡 Using default configuration")
    
    return default_config


def save_config(config: dict, path="config.json"):
    """Save configuration to file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Configuration saved to {path}")
    except Exception as e:
        print(f"❌ Failed to save config: {e}")


def validate_config(config: dict) -> bool:
    """Validate configuration structure."""
    required_keys = {
        "settings": ["memory_enabled"],
        "api": ["provider", "model"]
    }
    
    for section, keys in required_keys.items():
        if section not in config:
            print(f"❌ Missing config section: {section}")
            return False
        
        for key in keys:
            if key not in config[section]:
                print(f"❌ Missing config key: {section}.{key}")
                return False
    
    # Validate values
    if config["api"]["provider"] not in ["ollama"]:
        print(f"❌ Unsupported provider: {config['api']['provider']}")
        return False
    
    return True