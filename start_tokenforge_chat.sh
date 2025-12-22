#!/bin/bash
# Start TokenForge Chat Application

echo "🔥 Starting TokenForge Chat Application..."

# Check if tokenforge is installed
if ! python3 -c "import tokenforge" 2>/dev/null; then
    echo "⚠️  TokenForge not found. Installing..."
    cd tokenforge
    pip install -e . || {
        echo "❌ Failed to install TokenForge"
        exit 1
    }
    cd ..
fi

# Check if gradio is installed
if ! python3 -c "import gradio" 2>/dev/null; then
    echo "⚠️  Gradio not found. Installing..."
    pip install gradio>=4.0.0 || {
        echo "❌ Failed to install Gradio"
        exit 1
    }
fi

# Run the application
echo "🚀 Launching TokenForge Chat..."
python3 tokenforge_chat_app.py


