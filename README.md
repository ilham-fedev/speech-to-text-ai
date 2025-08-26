# Speech-to-Text AI App

A real-time speech recognition application with AI integration, supporting English and Indonesian languages.

## Features

- **Real-time Speech Recognition** - Live audio capture and transcription
- **Dual AI Modes**:
  - Basic: Google Speech Recognition API
  - Enhanced: OpenAI Whisper AI model
- **Multi-language Support** - English and Indonesian
- **User-friendly GUI** - Simple tkinter interface with start/stop controls
- **Timestamped Transcriptions** - Each transcription includes timestamp
- **Text Export** - Save transcriptions to text files
- **Thread-safe Implementation** - Stable operation without crashes

## Installation

### Prerequisites

- Python 3.8+
- macOS with Homebrew (for system dependencies)
- Microphone access permissions

### Quick Install

```bash
./install.sh
```

### Manual Installation

1. **Install system dependencies:**
   ```bash
   brew install portaudio ffmpeg
   ```

2. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   pip install pyaudio
   ```

### Troubleshooting

- **PyAudio build errors**: Ensure PortAudio is installed (`brew install portaudio`)
- **Whisper ffmpeg errors**: Install ffmpeg (`brew install ffmpeg`)
- **Permission errors**: Grant microphone access in System Preferences

## Usage

1. **Start the application:**
   ```bash
   python main.py
   ```

2. **Select recognition mode:**
   - Basic: Fast, internet-required
   - AI Enhanced: More accurate, works offline after model download

3. **Choose language:**
   - English (en-US)
   - Indonesian (id-ID)

4. **Record and transcribe:**
   - Click "Start Recording" to begin
   - Speak clearly into your microphone
   - Click "Stop Recording" to end
   - View timestamped transcriptions in the text area

5. **Export results:**
   - Click "Export Text" to save transcriptions to a file

## Dependencies

### Core Libraries
- `speechrecognition` - Google Speech API integration
- `openai-whisper` - AI-powered speech recognition
- `pyaudio` - Audio input/output handling
- `torch` & `torchaudio` - AI model backend
- `tkinter` - GUI framework (built-in with Python)

### Development Tools
- `flake8` - Code linting
- `black` - Code formatting
- `isort` - Import sorting

## Development

### Code Quality

Run linting and formatting:
```bash
./lint.sh
```

Or manually:
```bash
flake8 main.py
black main.py
isort main.py
```

### Project Structure

```
├── main.py           # Main application file
├── requirements.txt  # Python dependencies
├── install.sh       # Installation script
├── lint.sh          # Linting script
├── pyproject.toml   # Tool configuration
└── .gitignore       # Git ignore rules
```

## Technical Notes

- **Threading**: Uses queue-based communication for thread-safe GUI updates
- **AI Models**: Whisper runs on CPU with FP32 precision for compatibility
- **Audio Processing**: Temporary files are automatically cleaned up
- **Error Handling**: Graceful fallback from Whisper to Google Speech Recognition

## System Requirements

- **OS**: macOS (tested), Linux (should work), Windows (may require modifications)
- **RAM**: 4GB+ recommended (for Whisper AI model)
- **Storage**: ~1GB for Whisper models
- **Network**: Required for Google Speech Recognition mode

## License

MIT License - Feel free to use and modify as needed.