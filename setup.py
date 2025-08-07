"""
Setup script for the Quote Poster Generator application.
"""
import os
from setuptools import setup, find_packages

def read(fname):
    """Read the contents of a file."""
    with open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8') as f:
        return f.read()

setup(
    name="quote-poster-generator",
    version="1.0.0",
    author="MQPG",
    author_email="info@mqpg.com",
    description="A desktop application for creating beautiful quote posters with custom backgrounds or AI-generated images.",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quote-poster-generator",
    packages=find_packages(include=['app', 'app.*']),
    package_data={
        'app': [
            'assets/backgrounds/*',
            'assets/fonts/*',
            'assets/icons/*',
            'assets/styles/*',
        ]
    },
    install_requires=[
        'PyQt6>=6.4.0',
        'Pillow>=9.0.0',
        'python-dotenv>=1.0.0',
        'openai>=0.28.0',
        'requests>=2.28.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.910',
            'pylint>=2.12.0',
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=1.0.0',
        ],
    },
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'quote-poster=app.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Graphics',
    ],
    keywords='quote poster generator ai image-editing',
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/quote-poster-generator/issues',
        'Source': 'https://github.com/yourusername/quote-poster-generator',
    },
)
