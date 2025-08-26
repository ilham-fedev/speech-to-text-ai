#!/bin/bash

echo "Installing system dependencies for macOS..."
brew install portaudio ffmpeg

echo "Installing Python packages..."
pip install -r requirements.txt

echo "Installing PyAudio separately..."
pip install pyaudio

echo "Installing development tools..."
pip install flake8 black isort

echo "Installation complete! Run 'python main.py' to start the app."