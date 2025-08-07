"""
Core functionality for generating quote posters.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple
from pathlib import Path

from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QImage
from PyQt6.QtCore import Qt

class TextAlignment(Enum):
    """Text alignment options."""
    LEFT = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
    CENTER = Qt.AlignmentFlag.AlignCenter
    RIGHT = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

@dataclass
class PosterSettings:
    """Settings for generating a quote poster."""
    text: str = ""
    font_family: str = "Arial"
    font_size: int = 24
    text_color: QColor = QColor("white")
    alignment: TextAlignment = TextAlignment.CENTER
    padding: int = 40
    background_color: QColor = QColor("#333333")
    size: Tuple[int, int] = (800, 600)

class PosterGenerator:
    """Handles the generation of quote posters."""
    
    def __init__(self, settings: Optional[PosterSettings] = None):
        """Initialize with optional settings."""
        self.settings = settings or PosterSettings()
    
    def set_background_from_file(self, file_path: str) -> bool:
        """Set the background from an image file.
        
        Args:
            file_path: Path to the image file.
            
        Returns:
            bool: True if the background was set successfully, False otherwise.
        """
        if not Path(file_path).exists():
            return False
            
        self.background = QPixmap(file_path)
        return not self.background.isNull()
    
    def set_background_from_pixmap(self, pixmap: QPixmap) -> None:
        """Set the background from a QPixmap.
        
        Args:
            pixmap: The QPixmap to use as background.
        """
        self.background = pixmap
    
    def generate_poster(self) -> QPixmap:
        """Generate a poster with the current settings.
        
        Returns:
            QPixmap: The generated poster.
        """
        # Create a blank image if no background is set
        if not hasattr(self, 'background') or self.background.isNull():
            pixmap = QPixmap(*self.settings.size)
            pixmap.fill(self.settings.background_color)
        else:
            # Scale the background to the desired size while maintaining aspect ratio
            pixmap = self.background.scaled(
                *self.settings.size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Crop to the exact size if needed
            if pixmap.size() != self.settings.size:
                x = (pixmap.width() - self.settings.size[0]) // 2
                y = (pixmap.height() - self.settings.size[1]) // 2
                pixmap = pixmap.copy(x, y, *self.settings.size)
        
        # If there's no text, return the background as is
        if not self.settings.text.strip():
            return pixmap
        
        # Create a painter to draw on the pixmap
        painter = QPainter(pixmap)
        
        try:
            # Set up the font
            font = QFont(self.settings.font_family, self.settings.font_size)
            painter.setFont(font)
            painter.setPen(self.settings.text_color)
            
            # Set up text rectangle with padding
            rect = pixmap.rect().adjusted(
                self.settings.padding,
                self.settings.padding,
                -self.settings.padding,
                -self.settings.padding
            )
            
            # Draw the text with word wrap and alignment
            painter.drawText(
                rect,
                self.settings.alignment.value | Qt.TextFlag.TextWordWrap,
                self.settings.text
            )
            
        finally:
            painter.end()
        
        return pixmap
    
    def save_poster(self, file_path: str, format: str = "PNG") -> bool:
        """Save the generated poster to a file.
        
        Args:
            file_path: Path where to save the file.
            format: Image format (e.g., "PNG", "JPEG").
            
        Returns:
            bool: True if the file was saved successfully, False otherwise.
        """
        try:
            poster = self.generate_poster()
            return poster.save(file_path, format)
        except Exception as e:
            print(f"Error saving poster: {e}")
            return False
