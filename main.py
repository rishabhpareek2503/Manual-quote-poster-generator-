#!/usr/bin/env python3
"""
Main entry point for the Quote Poster Generator application.
"""
import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from app.ui.main_window import MainWindow

def main():
    """Initialize and start the application."""
    # Set up the application
    app = QApplication(sys.argv)
    
    # Set application information
    app.setApplicationName("Quote Poster Generator")
    app.setApplicationVersion("1.0.0")
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
