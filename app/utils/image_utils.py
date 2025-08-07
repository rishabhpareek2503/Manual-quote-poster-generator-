"""
Image processing utilities for the Quote Poster Generator.
"""
from typing import Optional, Tuple, Union
from pathlib import Path

from PyQt6.QtGui import QPixmap, QImage, QPainter, QColor, QFont, QFontMetrics
from PyQt6.QtCore import Qt, QRect, QSize

def resize_pixmap(pixmap: QPixmap, size: QSize, 
                 aspect_ratio_mode: Qt.AspectRatioMode = Qt.AspectRatioMode.KeepAspectRatio,
                 transform_mode: Qt.TransformationMode = Qt.TransformationMode.SmoothTransformation) -> QPixmap:
    """Resize a QPixmap while maintaining aspect ratio.
    
    Args:
        pixmap: The pixmap to resize.
        size: The target size (width, height).
        aspect_ratio_mode: How to handle aspect ratio.
        transform_mode: The transformation mode.
        
    Returns:
        QPixmap: The resized pixmap.
    """
    if pixmap.isNull():
        return pixmap
    
    return pixmap.scaled(size, aspect_ratio_mode, transform_mode)

def add_text_to_image(pixmap: QPixmap, text: str, 
                    font: QFont, 
                    text_color: QColor = QColor("white"),
                    alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter,
                    padding: int = 40) -> QPixmap:
    """Add text to an image.
    
    Args:
        pixmap: The image to add text to.
        text: The text to add.
        font: The font to use for the text.
        text_color: The color of the text.
        alignment: The alignment of the text.
        padding: The padding around the text.
        
    Returns:
        QPixmap: The image with text added.
    """
    if pixmap.isNull() or not text.strip():
        return pixmap
    
    # Create a copy of the pixmap to avoid modifying the original
    result = pixmap.copy()
    
    # Create a painter to draw on the pixmap
    painter = QPainter(result)
    try:
        painter.setFont(font)
        painter.setPen(text_color)
        
        # Set up text rectangle with padding
        rect = result.rect().adjusted(
            padding, padding, -padding, -padding
        )
        
        # Draw the text with word wrap and alignment
        painter.drawText(
            rect,
            alignment | Qt.TextFlag.TextWordWrap,
            text
        )
    finally:
        painter.end()
    
    return result

def create_gradient_pixmap(size: QSize, 
                          start_color: QColor, 
                          end_color: QColor,
                          direction: Qt.Orientation = Qt.Orientation.Vertical) -> QPixmap:
    """Create a gradient pixmap.
    
    Args:
        size: The size of the pixmap.
        start_color: The starting color of the gradient.
        end_color: The ending color of the gradient.
        direction: The direction of the gradient.
        
    Returns:
        QPixmap: A pixmap with a gradient fill.
    """
    image = QImage(size, QImage.Format.Format_RGB32)
    
    # Create a painter to draw the gradient
    painter = QPainter(image)
    try:
        # Set up the gradient
        if direction == Qt.Orientation.Vertical:
            gradient = QLinearGradient(0, 0, 0, size.height())
        else:
            gradient = QLinearGradient(0, 0, size.width(), 0)
        
        gradient.setColorAt(0, start_color)
        gradient.setColorAt(1, end_color)
        
        # Fill the image with the gradient
        painter.fillRect(0, 0, size.width(), size.height(), gradient)
    finally:
        painter.end()
    
    return QPixmap.fromImage(image)

def calculate_text_rect(text: str, 
                       font: QFont, 
                       max_width: int, 
                       max_height: int) -> QRect:
    """Calculate the bounding rectangle for text with word wrap.
    
    Args:
        text: The text to measure.
        font: The font to use.
        max_width: The maximum width of the text rectangle.
        max_height: The maximum height of the text rectangle.
        
    Returns:
        QRect: The bounding rectangle for the text.
    """
    if not text.strip():
        return QRect(0, 0, 0, 0)
    
    # Create a temporary pixmap to calculate text metrics
    temp_pixmap = QPixmap(1, 1)
    painter = QPainter(temp_pixmap)
    try:
        painter.setFont(font)
        metrics = painter.fontMetrics()
        
        # Calculate the bounding rectangle for the text with word wrap
        rect = metrics.boundingRect(
            0, 0, max_width, max_height,
            Qt.TextFlag.TextWordWrap | Qt.AlignmentFlag.AlignLeft,
            text
        )
    finally:
        painter.end()
    
    return rect

def load_pixmap_from_file(file_path: Union[str, Path], 
                         size: Optional[QSize] = None) -> Optional[QPixmap]:
    """Load a pixmap from a file, optionally resizing it.
    
    Args:
        file_path: Path to the image file.
        size: Optional target size for the pixmap.
        
    Returns:
        Optional[QPixmap]: The loaded pixmap, or None if loading failed.
    """
    file_path = str(file_path)
    
    if not Path(file_path).exists():
        return None
    
    pixmap = QPixmap(file_path)
    
    if pixmap.isNull():
        return None
    
    if size is not None:
        return resize_pixmap(pixmap, size)
    
    return pixmap

def save_pixmap(pixmap: QPixmap, 
               file_path: Union[str, Path], 
               quality: int = 90) -> bool:
    """Save a pixmap to a file.
    
    Args:
        pixmap: The pixmap to save.
        file_path: Path where to save the file.
        quality: Quality for JPEG compression (1-100).
        
    Returns:
        bool: True if the save was successful, False otherwise.
    """
    if pixmap.isNull():
        return False
    
    file_path = str(file_path)
    
    try:
        # Ensure the directory exists
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Determine format from file extension
        ext = Path(file_path).suffix.lower()
        
        if ext in ['.jpg', '.jpeg']:
            format = 'JPEG'
            quality = max(1, min(100, quality))  # Ensure quality is between 1-100
            return pixmap.save(file_path, format, quality=quality)
        else:
            # Default to PNG for other formats
            if ext != '.png':
                file_path = str(Path(file_path).with_suffix('.png'))
            return pixmap.save(file_path, 'PNG')
    except Exception as e:
        print(f"Error saving image to {file_path}: {e}")
        return False
