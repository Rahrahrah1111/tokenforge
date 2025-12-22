#!/bin/bash
# Stealth transcription runner - hides process with password

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source venv/bin/activate

# Run with stealth runner (password is empty string by default)
python3 stealth_runner.py fast_transcribe.py "$@" --password '' --background

