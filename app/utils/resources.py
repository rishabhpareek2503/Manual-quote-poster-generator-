"""
Resource management for the Quote Poster Generator.
"""
import os
import sys
import importlib.resources as pkg_resources
from pathlib import Path
from typing import Optional, Union, List, Dict, Any

from PyQt6.QtGui import QPixmap, QIcon, QFontDatabase, QFont
from PyQt6.QtCore import QFile, QIODevice, QByteArray

class ResourceManager:
    """Manages application resources like images, icons, and fonts."""
    
    def __init__(self, app_root: Optional[Union[str, Path]] = None):
        """Initialize the resource manager.
        
        Args:
            app_root: The root directory of the application.
        """
        self.app_root = Path(app_root) if app_root else self._find_app_root()
        self.resource_dirs = {
            'images': self.app_root / 'assets' / 'images',
            'backgrounds': self.app_root / 'assets' / 'backgrounds',
            'fonts': self.app_root / 'assets' / 'fonts',
            'icons': self.app_root / 'assets' / 'icons',
            'styles': self.app_root / 'assets' / 'styles'
        }
        
        # Ensure resource directories exist
        self._ensure_resource_dirs()
        
        # Loaded resources cache
        self._resource_cache = {}
        self._loaded_fonts = set()
    
    def _find_app_root(self) -> Path:
        """Find the application root directory.
        
        Returns:
            Path: The path to the application root directory.
        """
        # Try to find the root by looking for the assets directory
        current = Path(__file__).parent
        while current != current.parent:
            if (current / 'assets').exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _ensure_resource_dirs(self) -> None:
        """Ensure all resource directories exist."""
        for dir_path in self.resource_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def get_path(self, resource_type: str, *path_parts: str) -> Path:
        """Get the path to a resource.
        
        Args:
            resource_type: Type of resource ('images', 'backgrounds', 'fonts', 'icons', 'styles').
            *path_parts: Additional path components.
            
        Returns:
            Path: The full path to the resource.
            
        Raises:
            ValueError: If the resource type is invalid.
        """
        if resource_type not in self.resource_dirs:
            raise ValueError(f"Invalid resource type: {resource_type}")
            
        return self.resource_dirs[resource_type].joinpath(*path_parts)
    
    def load_pixmap(self, resource_type: str, *path_parts: str) -> Optional[QPixmap]:
        """Load a pixmap from resources.
        
        Args:
            resource_type: Type of resource ('images', 'backgrounds').
            *path_parts: Path components to the resource.
            
        Returns:
            Optional[QPixmap]: The loaded pixmap, or None if loading failed.
        """
        cache_key = f"pixmap:{resource_type}:{'/'.join(path_parts)}"
        
        # Check cache first
        if cache_key in self._resource_cache:
            return self._resource_cache[cache_key]
        
        # Load the pixmap
        file_path = self.get_path(resource_type, *path_parts)
        if not file_path.exists():
            return None
            
        pixmap = QPixmap(str(file_path))
        if not pixmap.isNull():
            self._resource_cache[cache_key] = pixmap
            return pixmap
            
        return None
    
    def load_icon(self, *path_parts: str, size: Optional[int] = None) -> Optional[QIcon]:
        """Load an icon from resources.
        
        Args:
            *path_parts: Path components to the icon file.
            size: Optional size for the icon.
            
        Returns:
            Optional[QIcon]: The loaded icon, or None if loading failed.
        """
        cache_key = f"icon:{'/'.join(path_parts)}:{size if size else ''}"
        
        # Check cache first
        if cache_key in self._resource_cache:
            return self._resource_cache[cache_key]
        
        # Load the icon
        file_path = self.get_path('icons', *path_parts)
        if not file_path.exists():
            return None
            
        if size:
            pixmap = QPixmap(str(file_path)).scaled(
                size, size, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            icon = QIcon(pixmap)
        else:
            icon = QIcon(str(file_path))
            
        if not icon.isNull():
            self._resource_cache[cache_key] = icon
            return icon
            
        return None
    
    def load_font(self, *path_parts: str) -> bool:
        """Load a font from resources.
        
        Args:
            *path_parts: Path components to the font file.
            
        Returns:
            bool: True if the font was loaded successfully, False otherwise.
        """
        font_path = str(self.get_path('fonts', *path_parts))
        
        # Check if already loaded
        if font_path in self._loaded_fonts:
            return True
            
        # Load the font
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            self._loaded_fonts.add(font_path)
            return True
            
        return False
    
    def get_font_families(self) -> List[str]:
        """Get a list of available font families.
        
        Returns:
            List[str]: List of font family names.
        """
        return QFontDatabase.families()
    
    def load_style_sheet(self, *path_parts: str) -> str:
        """Load a style sheet from resources.
        
        Args:
            *path_parts: Path components to the style sheet file.
            
        Returns:
            str: The contents of the style sheet, or an empty string if loading failed.
        """
        file_path = self.get_path('styles', *path_parts)
        if not file_path.exists():
            return ""
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except (IOError, UnicodeDecodeError):
            return ""
    
    def get_backgrounds(self) -> List[Dict[str, Any]]:
        """Get a list of available backgrounds.
        
        Returns:
            List[Dict[str, Any]]: List of background information dictionaries.
        """
        backgrounds = []
        bg_dir = self.resource_dirs['backgrounds']
        
        for file_path in bg_dir.glob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp']:
                backgrounds.append({
                    'name': file_path.stem,
                    'path': str(file_path),
                    'thumbnail': self.load_pixmap('backgrounds', file_path.name)
                })
                
        return backgrounds
    
    def get_default_background(self) -> Optional[QPixmap]:
        """Get the default background.
        
        Returns:
            Optional[QPixmap]: The default background pixmap, or None if not found.
        """
        # Try to load a default background if it exists
        default_bg = self.load_pixmap('images', 'default_background.png')
        if default_bg and not default_bg.isNull():
            return default_bg
            
        # If no default background exists, create a simple gradient
        from PyQt6.QtGui import QLinearGradient
        from PyQt6.QtCore import QPointF
        
        pixmap = QPixmap(800, 600)
        pixmap.fill(Qt.GlobalColor.white)
        
        painter = QPainter(pixmap)
        try:
            gradient = QLinearGradient(QPointF(0, 0), QPointF(800, 600))
            gradient.setColorAt(0, QColor(74, 144, 226))  # Blue
            gradient.setColorAt(1, QColor(28, 62, 148))   # Darker blue
            
            painter.fillRect(0, 0, 800, 600, gradient)
        finally:
            painter.end()
            
        return pixmap
