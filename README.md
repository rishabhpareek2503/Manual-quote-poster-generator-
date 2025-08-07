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

## License

This project is licensed under the MIT License.
├── app/                    # Main application package
│   ├── core/              # Core business logic
│   │   ├── ai_generator.py  # AI background generation
│   │   └── poster_generator.py  # Image processing
│   │
│   ├── ui/                # User interface components
│   │   ├── main_window.py  # Main application window
│   │   └── dialogs/       # Various dialog windows
│   │
│   ├── utils/             # Utility functions
│   │   ├── config.py     # Configuration management
│   │   ├── file_utils.py # File operations
│   │   └── resources.py  # Resource management
│   │
│   ├── __init__.py
│   └── application.py    # Application class
│
├── assets/                # Static assets
│   ├── backgrounds/      # Default background images
│   ├── fonts/           # Custom fonts
│   ├── icons/           # Application icons
│   └── styles/          # CSS stylesheets
│
├── output/               # Default export directory
├── tests/               # Test files
│
├── .env                 # Environment variables
├── .gitignore
├── LICENSE
├── main.py             # Application entry point
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Required for AI background generation
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Custom paths
BACKGROUNDS_DIR=path/to/custom/backgrounds
EXPORT_DIR=path/to/export/folder
```

### Application Settings

Most settings can be configured through the application's Settings dialog. These include:
- Default save locations
- Recent files history
- UI preferences
- AI generation settings

## Development

### Setting Up for Development

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Run with debug mode:
   ```bash
   python -m app.main --debug
   ```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- AI background generation powered by [OpenAI DALL-E 3](https://openai.com/dall-e-3)
- Icons from [Material Design Icons](https://materialdesignicons.com/)

---

*Created with ❤️ by MQPG*
