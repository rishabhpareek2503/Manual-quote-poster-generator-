"""
Configuration management for the Quote Poster Generator.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

from PyQt6.QtCore import QSettings, QStandardPaths

class ConfigManager:
    """Manages application configuration and settings."""
    
    def __init__(self, app_name: str = "QuotePosterGenerator"):
        """Initialize the configuration manager.
        
        Args:
            app_name: Name of the application for settings organization.
        """
        self.app_name = app_name
        self.settings = QSettings("MQPG", app_name)
        self.app_data_dir = self._get_app_data_dir()
        self.config_file = os.path.join(self.app_data_dir, 'config.json')
        self.default_settings = {
            'recent_files': [],
            'max_recent_files': 10,
            'default_save_dir': str(Path.home() / 'Pictures' / 'QuotePosters'),
            'default_font': 'Arial',
            'default_font_size': 24,
            'default_text_color': '#FFFFFF',
            'default_bg_color': '#333333',
            'window_geometry': None,
            'window_state': None,
        }
        self._ensure_config_file_exists()
    
    def _get_app_data_dir(self) -> str:
        """Get the application data directory, creating it if it doesn't exist.
        
        Returns:
            str: Path to the application data directory.
        """
        app_data = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        
        if not os.path.exists(app_data):
            os.makedirs(app_data, exist_ok=True)
        
        return app_data
    
    def _ensure_config_file_exists(self) -> None:
        """Ensure the config file exists with default values if it doesn't."""
        if not os.path.exists(self.config_file):
            self._save_config(self.default_settings)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load the configuration from file.
        
        Returns:
            Dict[str, Any]: The loaded configuration.
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Merge with default settings to ensure all keys exist
            merged = {**self.default_settings, **config}
            return merged
        except (json.JSONDecodeError, FileNotFoundError):
            return self.default_settings.copy()
    
    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save the configuration to file.
        
        Args:
            config: The configuration to save.
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except (IOError, TypeError) as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: The configuration key.
            default: Default value if the key doesn't exist.
            
        Returns:
            The configuration value, or the default if not found.
        """
        config = self._load_config()
        return config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.
        
        Args:
            key: The configuration key.
            value: The value to set.
        """
        config = self._load_config()
        config[key] = value
        self._save_config(config)
    
    def add_recent_file(self, file_path: str) -> None:
        """Add a file to the recent files list.
        
        Args:
            file_path: Path to the file to add.
        """
        recent_files = self.get('recent_files', [])
        
        # Remove if already exists
        if file_path in recent_files:
            recent_files.remove(file_path)
        
        # Add to the beginning
        recent_files.insert(0, file_path)
        
        # Trim the list if it's too long
        max_files = self.get('max_recent_files', 10)
        if len(recent_files) > max_files:
            recent_files = recent_files[:max_files]
        
        self.set('recent_files', recent_files)
    
    def get_recent_files(self) -> list:
        """Get the list of recent files.
        
        Returns:
            list: List of recent file paths.
        """
        return self.get('recent_files', [])
    
    def clear_recent_files(self) -> None:
        """Clear the recent files list."""
        self.set('recent_files', [])
    
    def save_window_geometry(self, geometry: bytes, state: bytes) -> None:
        """Save the main window geometry and state.
        
        Args:
            geometry: The window geometry as bytes.
            state: The window state as bytes.
        """
        self.set('window_geometry', geometry.hex())
        self.set('window_state', state.hex())
    
    def load_window_geometry(self) -> Optional[bytes]:
        """Load the saved window geometry.
        
        Returns:
            Optional[bytes]: The window geometry as bytes, or None if not found.
        """
        geometry_hex = self.get('window_geometry')
        if geometry_hex:
            return bytes.fromhex(geometry_hex)
        return None
    
    def load_window_state(self) -> Optional[bytes]:
        """Load the saved window state.
        
        Returns:
            Optional[bytes]: The window state as bytes, or None if not found.
        """
        state_hex = self.get('window_state')
        if state_hex:
            return bytes.fromhex(state_hex)
        return None
