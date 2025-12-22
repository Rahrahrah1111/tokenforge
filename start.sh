#!/bin/bash

# A.V.A. Startup Script
# Starts Ollama and the web server with API keys loaded

echo "🚀 A.V.A. - Autonomous Virtual Avatar"
echo "======================================"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load environment variables from .env if it exists
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ Loading API keys from .env${NC}"
    export $(grep -v '^#' .env | xargs)
else
    echo -e "${YELLOW}⚠ No .env file found. Some features may be limited.${NC}"
    echo -e "${YELLOW}  Copy .env.example to .env and add your API keys${NC}"
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}✗ Ollama not installed${NC}"
    echo "  Install with: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

# Start Ollama if not running (with CORS enabled for browser access)
if ! pgrep -x "ollama" > /dev/null; then
    echo -e "${CYAN}Starting Ollama server with CORS enabled...${NC}"
    OLLAMA_ORIGINS="*" ollama serve &
    sleep 3
else
    echo -e "${GREEN}✓ Ollama already running${NC}"
    # Restart with CORS if needed
    echo -e "${YELLOW}Restarting Ollama with CORS enabled...${NC}"
    killall ollama 2>/dev/null
    sleep 1
    OLLAMA_ORIGINS="*" ollama serve &
    sleep 3
fi

# Check for models
MODELS=$(ollama list 2>/dev/null | tail -n +2)
if [ -z "$MODELS" ]; then
    echo -e "${YELLOW}⚠ No Ollama models found. Pulling llama3.2:3b...${NC}"
    ollama pull llama3.2:3b
else
    echo -e "${GREEN}✓ Available models:${NC}"
    echo "$MODELS" | head -5
fi

# Test Ollama connection
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama API responding${NC}"
else
    echo -e "${RED}✗ Ollama API not responding${NC}"
fi

# Kill any existing http server on port 8080
if lsof -i :8080 > /dev/null 2>&1; then
    echo -e "${YELLOW}Stopping existing server on port 8080...${NC}"
    fuser -k 8080/tcp 2>/dev/null
    sleep 1
fi

# Start HTTP server
echo -e "${CYAN}Starting web server on http://localhost:8080${NC}"
echo ""
echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}  A.V.A. is ready!${NC}"
echo -e "${GREEN}  Open: http://localhost:8080${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Start Python HTTP server
python3 -m http.server 8080

