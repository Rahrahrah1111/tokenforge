# Wyze Camera Analyzer

A comprehensive application for analyzing Wyze Cam Pan v3 footage, detecting events, transcribing speech, and organizing results.

## Features

- **Video Analysis**: Process video footage from SD card, API, or cloud services
- **Event Detection**: Automatically detect and categorize events (motion, human detection, etc.)
- **Speech Transcription**: Transcribe human speech using OpenAI Whisper
- **Audio Enhancement**: Improve audio quality with noise reduction, amplification, and filtering
- **Event Organization**: Automatically organize events into categorized folders
- **Web Dashboard**: View and manage analysis results through a web interface
- **Long-term Analysis**: Process up to 2 weeks (or more) of video footage

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for video/audio processing)
- CUDA-capable GPU (optional, for faster transcription)

### Quick Setup

Run the automated setup script:

```bash
cd "/home/g-spot/Downloads/OKComputer_A.V.A. Chat Integration/wyze_analyzer"
chmod +x setup.sh
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up everything automatically

### Manual Setup

If you prefer to set up manually:

1. **Install FFmpeg:**

   **Linux:**
   ```bash
   sudo apt-get update
   sudo apt-get install ffmpeg
   ```

   **macOS:**
   ```bash
   brew install ffmpeg
   ```

   **Windows:**
   Download from [FFmpeg website](https://ffmpeg.org/download.html)

2. **Create virtual environment:**
   ```bash
   cd "/home/g-spot/Downloads/OKComputer_A.V.A. Chat Integration/wyze_analyzer"
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.yaml` to configure:

- Video source (SD card path, API credentials, or cloud settings)
- Analysis period (default: 14 days)
- Event detection sensitivity
- Audio enhancement settings
- Transcription model (tiny/base/small/medium/large)
- Output directory structure

## Usage

**Important:** Always activate the virtual environment first:
```bash
cd "/home/g-spot/Downloads/OKComputer_A.V.A. Chat Integration/wyze_analyzer"
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Basic Usage (SD Card)

1. Insert your Wyze camera's SD card into your computer
2. Run the analyzer:

```bash
# Using the quick start script (recommended)
./run_analyzer.sh /path/to/sd/card

# Or directly with Python
python main.py /path/to/sd/card
```

### Analyze Specific Date Range

```bash
python main.py /path/to/sd/card --start-date 2024-01-01 --end-date 2024-01-14
```

### Analyze Last N Days

```bash
python main.py /path/to/sd/card --days 14
```

### Using Custom Config

```bash
python main.py /path/to/sd/card --config custom_config.yaml
```

## Web Interface

Start the web dashboard (make sure virtual environment is activated):

```bash
source venv/bin/activate  # If not already activated
python web_interface.py
```

Then open your browser to `http://localhost:5000`

The web interface allows you to:
- View all detected events
- Filter events by type and date
- View statistics
- Play video and audio clips
- Read transcriptions

## Output Structure

Events are organized in the output directory:

```
wyze_analysis_output/
├── 2024/
│   ├── 01/
│   │   ├── 15/
│   │   │   ├── motion/
│   │   │   │   ├── 20240115_143022_motion_120s_event_123_metadata.json
│   │   │   │   ├── 20240115_143022_motion_120s_event_123.mp4
│   │   │   │   ├── 20240115_143022_motion_120s_event_123_audio.wav
│   │   │   │   ├── 20240115_143022_motion_120s_event_123_transcription.json
│   │   │   │   └── 20240115_143022_motion_120s_event_123_transcription.txt
│   │   │   └── speech_detection/
│   │   │       └── ...
│   └── event_log.csv
```

## Event Types

The analyzer can detect and categorize:

- **motion**: General motion detection
- **human_detection**: Human presence
- **vehicle**: Vehicle detection
- **animal**: Animal detection
- **sound_detection**: Audio activity
- **speech_detection**: Human speech
- **package_delivery**: Package delivery events
- **door_opening**: Door activity
- **night_vision**: Night vision mode

## Audio Enhancement

The audio processor applies:

- **Noise Reduction**: Removes background noise
- **Amplification**: Boosts audio signal (configurable)
- **High-pass Filter**: Removes low-frequency noise (default: 80Hz)
- **Low-pass Filter**: Removes high-frequency noise (default: 8kHz)
- **Normalization**: Normalizes audio levels

## Transcription Models

Whisper model options (in order of quality/speed):

- **tiny**: Fastest, least accurate (~39M parameters)
- **base**: Good balance (~74M parameters)
- **small**: Better accuracy (~244M parameters)
- **medium**: High accuracy (~769M parameters)
- **large**: Best accuracy (~1550M parameters)

For best transcription quality, use `large` model (requires more RAM/VRAM).

## Performance Tips

1. **Use GPU**: Enable CUDA for faster transcription
2. **Adjust FPS**: Lower FPS in config for faster processing (less detailed)
3. **Chunk Processing**: Process videos in chunks to manage memory
4. **Model Selection**: Use smaller Whisper models for faster processing
5. **Parallel Processing**: Adjust `max_workers` in config for your CPU

## Troubleshooting

### FFmpeg not found
Make sure FFmpeg is installed and in your PATH.

### Out of memory
- Use smaller Whisper model
- Reduce `chunk_size` in config
- Process fewer videos at once

### Poor transcription quality
- Use larger Whisper model
- Increase audio amplification
- Adjust noise reduction settings
- Check audio quality in source video

### No events detected
- Lower `motion_threshold` in config
- Check video files are valid
- Verify date range includes video files

## API Integration (Future)

Wyze doesn't provide an official API, but community APIs exist:
- `wyze-api` Python library
- Custom API integrations

To use API, update `config.yaml`:
```yaml
video_source:
  source_type: "api"
  wyze_api:
    email: "your@email.com"
    password: "yourpassword"
```

## License

This project is provided as-is for personal use.

## Support

For issues or questions, check the logs in `wyze_analyzer.log`.

