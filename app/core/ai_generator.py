"""
AI-powered background generation for the Quote Poster Generator.
Supports both OpenAI and Azure OpenAI services.
"""
import os
import base64
import requests
from typing import Optional, Dict, Any, List, Tuple, Union
from dataclasses import dataclass
from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal, QThread, QSize
from PyQt6.QtGui import QPixmap, QImage

from openai import OpenAI, AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "dall-e-3")

@dataclass
class AIGenerationResult:
    """Represents the result of an AI image generation request."""
    success: bool
    image: Optional[QPixmap] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class AIGenerationError(Exception):
    """Exception raised for AI generation errors."""
    pass

class AIGenerator(QObject):
    """Handles AI-powered background generation."""
    
    # Signals
    generation_started = pyqtSignal()
    generation_finished = pyqtSignal(AIGenerationResult)
    progress_updated = pyqtSignal(int)  # 0-100
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI generator.
        
        Args:
            api_key: Optional API key. If not provided, will try to get from environment.
        """
        super().__init__()
        self.api_key = api_key or AZURE_OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        self._worker = None
        self._is_azure = bool(AZURE_OPENAI_ENDPOINT and self.api_key)
    
    def is_configured(self) -> bool:
        """Check if the AI generator is properly configured.
        
        Returns:
            bool: True if configured, False otherwise.
        """
        if self._is_azure:
            return bool(self.api_key and AZURE_OPENAI_ENDPOINT)
        return bool(self.api_key)
    
    def set_api_key(self, api_key: str) -> None:
        """Set the OpenAI API key.
        
        Args:
            api_key: The OpenAI API key.
        """
        self.api_key = api_key
    
    def generate_background(self, prompt: str, size: Tuple[int, int] = (1024, 1024)) -> None:
        """Generate a background image using AI.
        
        Args:
            prompt: The text prompt to generate an image from.
            size: The desired size of the generated image (width, height).
        """
        if not self.is_configured():
            result = AIGenerationResult(
                success=False,
                error="OpenAI API key not configured. Please set your API key in settings."
            )
            self.generation_finished.emit(result)
            return
        
        # Cancel any ongoing generation
        self.cancel_generation()
        
        # Create and start a worker thread
        self._worker = AIGenerationWorker(self.api_key, prompt, size, self._is_azure)
        self._worker.finished.connect(self._on_generation_finished)
        self._worker.progress_updated.connect(self.progress_updated.emit)
        
        self.generation_started.emit()
        self._worker.start()
    
    def cancel_generation(self) -> None:
        """Cancel the current generation process."""
        if self._worker and self._worker.isRunning():
            self._worker.cancel()
            self._worker.wait()
    
    def _on_generation_finished(self, result: AIGenerationResult) -> None:
        """Handle the completion of a generation task.
        
        Args:
            result: The generation result.
        """
        self._worker = None
        self.generation_finished.emit(result)

class AIGenerationWorker(QThread):
    """Worker thread for AI generation tasks."""
    
    finished = pyqtSignal(AIGenerationResult)
    progress_updated = pyqtSignal(int)
    
    def __init__(self, api_key: str, prompt: str, size: Tuple[int, int], is_azure: bool):
        """Initialize the worker.
        
        Args:
            api_key: The OpenAI API key.
            prompt: The text prompt for image generation.
            size: The desired image size (width, height).
            is_azure: Whether to use Azure OpenAI.
        """
        super().__init__()
        self.api_key = api_key
        self.prompt = prompt
        self.size = size
        self._is_azure = is_azure
        self._is_cancelled = False
    
    def run(self) -> None:
        """Run the generation task."""
        try:
            self.progress_updated.emit(10)
            
            if self._is_azure and AZURE_OPENAI_ENDPOINT and self.api_key:
                # Azure OpenAI client
                client = AzureOpenAI(
                    api_key=self.api_key,
                    api_version=AZURE_OPENAI_API_VERSION,
                    azure_endpoint=AZURE_OPENAI_ENDPOINT,
                )
                
                # Azure OpenAI requires a deployment name
                response = client.images.generate(
                    model=AZURE_DEPLOYMENT_NAME,
                    prompt=self.prompt,
                    size=f"{self.size[0]}x{self.size[1]}",
                    quality="standard",
                    n=1,
                    response_format="url"  # Request URL response format
                )
            elif self.api_key:
                # Standard OpenAI client
                client = OpenAI(api_key=self.api_key)
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=self.prompt,
                    size=f"{self.size[0]}x{self.size[1]}",
                    quality="standard",
                    n=1,
                    response_format="url"  # Request URL response format
                )
            else:
                raise AIGenerationError("No valid API configuration found")
            
            if self._is_cancelled:
                return
            
            self.progress_updated.emit(30)
            
            # Get the image URL from the response
            if not response.data or not hasattr(response.data[0], 'url') or not response.data[0].url:
                raise AIGenerationError("No image URL returned from API")
                
            image_url = response.data[0].url
            
            # Download the image
            headers = {}
            if 'openai.azure.com' in str(image_url):
                # Add API key as a query parameter for Azure OpenAI
                if '?' in image_url:
                    image_url += f"&api-version={AZURE_OPENAI_API_VERSION}"
                else:
                    image_url += f"?api-version={AZURE_OPENAI_API_VERSION}"
                headers["api-key"] = self.api_key
            
            # Download the image with proper headers
            image_response = requests.get(image_url, headers=headers)
            image_response.raise_for_status()
            image_data = image_response.content
            
            # Convert to QPixmap
            image = QImage()
            if not image.loadFromData(image_data):
                # Try different image formats if the default loading fails
                for fmt in [b'PNG', b'JPEG', b'BMP', b'GIF']:
                    if image.loadFromData(image_data, fmt):
                        break
                else:
                    raise AIGenerationError("Failed to load image data")
                    
            pixmap = QPixmap.fromImage(image)
            
            if pixmap.isNull():
                raise AIGenerationError("Failed to create valid image from response")
            
            if self._is_cancelled:
                return
            
            self.progress_updated.emit(90)
            
            # Create the result
            result = AIGenerationResult(
                success=True,
                image=pixmap,
                metadata={
                    "model": "dall-e-3",
                    "size": size_str,
                    "revised_prompt": getattr(response.data[0], 'revised_prompt', self.prompt)
                }
            )
            
            self.progress_updated.emit(100)
            self.finished.emit(result)
            
        except Exception as e:
            error_msg = str(e)
            if "rate_limit" in error_msg.lower():
                error_msg = "API rate limit exceeded. Please try again later."
            elif "invalid_api_key" in error_msg.lower():
                error_msg = "Invalid API key. Please check your API key in settings."
            elif "billing_hard_limit_reached" in error_msg.lower():
                error_msg = "Billing hard limit reached. Please check your OpenAI account."
            
            result = AIGenerationResult(
                success=False,
                error=f"AI generation failed: {error_msg}"
            )
            self.finished.emit(result)
    
    def cancel(self) -> None:
        """Cancel the generation task."""
        self._is_cancelled = True

# Example usage:
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Get API key from environment or user input
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API key: ")
    
    # Create and configure the generator
    generator = AIGenerator(api_key)
    
    # Connect signals
    def on_generation_started():
        print("Generation started...")
    
    def on_progress_updated(progress):
        print(f"Progress: {progress}%")
    
    def on_generation_finished(result):
        if result.success:
            print("Generation successful!")
            print(f"Image size: {result.image.size()}")
            if result.metadata:
                print(f"Revised prompt: {result.metadata.get('revised_prompt')}")
        else:
            print(f"Error: {result.error}")
        
        app.quit()
    
    generator.generation_started.connect(on_generation_started)
    generator.progress_updated.connect(on_progress_updated)
    generator.generation_finished.connect(on_generation_finished)
    
    # Start generation
    prompt = "A beautiful mountain landscape at sunset, digital art style"
    generator.generate_background(prompt, (1024, 1024))
    
    sys.exit(app.exec())
