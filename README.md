# Quote Poster Generator

A simple desktop application for creating beautiful quote posters with custom backgrounds. Built with Python and PyQt6.

## Features

- **Background Options**
  - Built-in background collection
  - Custom image support

- **Text Customization**
  - Multiple font families and sizes
  - Custom text colors
  - Text alignment (left, center, right)
  - Adjustable text position

- **Easy to Use**
  - Real-time preview
  - Simple and intuitive interface
  - Export to image (PNG, JPG)

## Installation

1. **Prerequisites**
   - Python 3.9 or higher
   - pip (Python package manager)

2. **Clone and install**
   ```bash
   git clone https://github.com/yourusername/quote-poster-generator.git
   cd quote-poster-generator
   pip install -r requirements.txt
   ```

## Quick Start

1. **Run the application**
   ```bash
   python main.py
   ```

2. **Create your poster**
   - Add a background (from collection or custom image)
   - Enter your quote text
   - Customize the text appearance
   - Adjust text position using the sliders
   - Export your creation!

## Project Structure

```
quote_poster_generator/
├── app/                  # Main application package
│   ├── core/             # Core functionality
│   ├── ui/               # User interface components
│   └── utils/            # Utility functions
├── assets/               # Background images and resources
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Required for AI background generation
OPENAI_API_KEY=your_openai_api_key_here


### Application Settings

Most settings can be configured through the application's Settings dialog. These include:
- Default save locations
- Recent files history
- UI preferences
- AI generation settings

