"""
Main application class for the Quote Poster Generator.
"""
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt, QSize, QSettings
from PyQt6.QtGui import QIcon, QAction, QPixmap

from .ui.main_window import MainWindow
from .utils.config import ConfigManager
from .utils.resources import ResourceManager

class QuotePosterApp(QApplication):
    """Main application class for the Quote Poster Generator."""
    
    def __init__(self, argv):
        """Initialize the application.
        
        Args:
            argv: Command line arguments.
        ""
        super().__init__(argv)
        
        # Set application information
        self.setApplicationName("Quote Poster Generator")
        self.setApplicationVersion("1.0.0")
        self.setOrganizationName("MQPG")
        
        # Initialize components
        self.config = ConfigManager()
        self.resource_manager = ResourceManager()
        
        # Create and show the main window
        self.main_window = MainWindow(self)
        
        # Load settings
        self.load_settings()
    
    def load_settings(self) -> None:
        """Load application settings."""
        # Load window geometry and state
        geometry = self.config.load_window_geometry()
        state = self.config.load_window_state()
        
        if geometry:
            self.main_window.restoreGeometry(geometry)
        if state:
            self.main_window.restoreState(state)
        
        # Center the window if no saved geometry
        if not geometry:
            screen = self.primaryScreen().availableGeometry()
            size = self.main_window.size()
            self.main_window.move(
                (screen.width() - size.width()) // 2,
                (screen.height() - size.height()) // 2
            )
    
    def save_settings(self) -> None:
        """Save application settings."""
        # Save window geometry and state
        self.config.save_window_geometry(
            self.main_window.saveGeometry(),
            self.main_window.saveState()
        )
    
    def run(self) -> int:
        """Run the application.
        
        Returns:
            int: Exit code.
        """
        self.main_window.show()
        return self.exec()
    
    def about_to_quit(self) -> None:
        """Handle application quit event."""
        self.save_settings()


def main():
    """Main entry point for the application."""
    # Create application instance
    app = QuotePosterApp(sys.argv)
    
    # Set up application style
    app.setStyle('Fusion')
    
    # Connect aboutToQuit signal
    app.aboutToQuit.connect(app.about_to_quit)
    
    # Run the application
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
