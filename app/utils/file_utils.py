"""
File utility functions for the Quote Poster Generator.
"""
import os
import shutil
from pathlib import Path
from typing import Optional, List, Tuple

from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

def ensure_directory_exists(directory: str) -> bool:
    """Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory.
        
    Returns:
        bool: True if the directory exists or was created, False otherwise.
    """
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except (OSError, Exception) as e:
        print(f"Error creating directory {directory}: {e}")
        return False

def get_supported_image_extensions() -> List[str]:
    """Get a list of supported image file extensions.
    
    Returns:
        List[str]: List of supported extensions (with leading dots).
    """
    return ['.png', '.jpg', '.jpeg', '.bmp', '.gif']

def is_supported_image_file(file_path: str) -> bool:
    """Check if a file has a supported image extension.
    
    Args:
        file_path: Path to the file.
        
    Returns:
        bool: True if the file has a supported image extension.
    """
    return any(file_path.lower().endswith(ext) for ext in get_supported_image_extensions())

def get_image_files(directory: str) -> List[str]:
    """Get a list of image files in a directory.
    
    Args:
        directory: Path to the directory to search.
        
    Returns:
        List[str]: List of paths to image files.
    """
    if not os.path.isdir(directory):
        return []
    
    return [
        os.path.join(directory, f) for f in os.listdir(directory)
        if is_supported_image_file(f) and os.path.isfile(os.path.join(directory, f))
    ]

def load_pixmap(file_path: str, size: Optional[Tuple[int, int]] = None) -> Optional[QPixmap]:
    """Load a QPixmap from a file, optionally resizing it.
    
    Args:
        file_path: Path to the image file.
        size: Optional (width, height) to resize the image to.
        
    Returns:
        Optional[QPixmap]: The loaded pixmap, or None if loading failed.
    """
    if not os.path.isfile(file_path) or not is_supported_image_file(file_path):
        return None
    
    pixmap = QPixmap(file_path)
    
    if pixmap.isNull():
        return None
    
    if size is not None:
        pixmap = pixmap.scaled(
            size[0], size[1],
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
    
    return pixmap

def save_pixmap(pixmap: QPixmap, file_path: str, quality: int = 90) -> bool:
    """Save a QPixmap to a file.
    
    Args:
        pixmap: The pixmap to save.
        file_path: Path where to save the file.
        quality: Quality for JPEG compression (1-100).
        
    Returns:
        bool: True if the save was successful, False otherwise.
    """
    if pixmap.isNull():
        return False
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # Determine format from file extension
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.jpg', '.jpeg']:
            format = 'JPEG'
            quality = max(1, min(100, quality))  # Ensure quality is between 1-100
            return pixmap.save(file_path, format, quality=quality)
        else:
            # Default to PNG for other formats
            if ext != '.png':
                file_path = os.path.splitext(file_path)[0] + '.png'
            return pixmap.save(file_path, 'PNG')
    except Exception as e:
        print(f"Error saving image to {file_path}: {e}")
        return False

def copy_file(src: str, dst: str) -> bool:
    """Copy a file from src to dst, creating directories if needed.
    
    Args:
        src: Source file path.
        dst: Destination file path.
        
    Returns:
        bool: True if the copy was successful, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"Error copying file from {src} to {dst}: {e}")
        return False
