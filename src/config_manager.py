import json
import os
from typing import Dict, Any
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path: str = "config/config.json"):
        self.config_path = config_path
        self.config: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found at {self.config_path}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON in configuration file {self.config_path}")

    def get_chats(self):
        """Get all configured chats."""
        return self.config.get('chats', [])

    def get_message_content(self):
        """Get configured message content."""
        return self.config.get('message_content', {})

    def save_config(self):
        """Save current configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2) 
