#!/bin/bash
# Quick start script for Wyze Camera Analyzer

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   ./setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: FFmpeg is not installed. Please install FFmpeg first."
    echo "Linux: sudo apt-get install ffmpeg"
    echo "macOS: brew install ffmpeg"
    exit 1
fi

# Run the analyzer
if [ -z "$1" ]; then
    echo "Usage: ./run_analyzer.sh /path/to/sd/card [--days N]"
    echo ""
    echo "Examples:"
    echo "  ./run_analyzer.sh /media/sd_card"
    echo "  ./run_analyzer.sh /media/sd_card --days 14"
    exit 1
fi

python main.py "$@"

