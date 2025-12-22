#!/bin/bash

# Complete Agent Zero Setup Script for Zorin Linux
# This script does everything needed to get Agent Zero running

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "═══════════════════════════════════════════════════════════"
echo "  Agent Zero Complete Setup"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check/Install Docker
echo "📦 Step 1: Checking Docker installation..."
if ! command_exists docker; then
    echo "   Docker not found. Installing Docker..."
    echo "   (You will be prompted for your password)"
    sudo apt update
    sudo apt install -y docker.io
    
    echo "   Starting Docker service..."
    sudo systemctl start docker
    sudo systemctl enable docker
    
    echo "   Adding user to docker group..."
    sudo usermod -aG docker $USER
    
    echo ""
    echo "   ⚠️  IMPORTANT: You need to log out and log back in"
    echo "      for docker group changes to take effect."
    echo ""
    echo "   For now, we'll use 'sudo' for docker commands."
    USE_SUDO="sudo"
else
    echo "   ✅ Docker is already installed"
    USE_SUDO=""
    
    # Check if we can run docker without sudo
    if docker info &>/dev/null; then
        echo "   ✅ Docker is accessible without sudo"
    else
        echo "   ⚠️  Docker requires sudo. Using sudo for commands."
        USE_SUDO="sudo"
    fi
fi

# Step 2: Check Docker daemon
echo ""
echo "🔍 Step 2: Checking Docker daemon..."
if $USE_SUDO docker info &>/dev/null; then
    echo "   ✅ Docker daemon is running"
else
    echo "   Starting Docker daemon..."
    sudo systemctl start docker
    sleep 2
    if $USE_SUDO docker info &>/dev/null; then
        echo "   ✅ Docker daemon started"
    else
        echo "   ❌ Failed to start Docker daemon"
        exit 1
    fi
fi

# Step 3: Check/Install Docker Compose
echo ""
echo "🔧 Step 3: Checking Docker Compose..."
if command_exists docker-compose; then
    COMPOSE_CMD="$USE_SUDO docker-compose"
    echo "   ✅ docker-compose found"
elif $USE_SUDO docker compose version &>/dev/null; then
    COMPOSE_CMD="$USE_SUDO docker compose"
    echo "   ✅ docker compose (plugin) found"
else
    echo "   Installing docker-compose..."
    sudo apt install -y docker-compose
    COMPOSE_CMD="$USE_SUDO docker-compose"
fi

# Step 4: Pull Agent Zero image
echo ""
echo "📥 Step 4: Pulling Agent Zero image..."
if $USE_SUDO docker pull agent0ai/agent-zero:latest; then
    echo "   ✅ Image pulled successfully"
else
    echo "   ❌ Failed to pull image"
    exit 1
fi

# Step 5: Start Agent Zero
echo ""
echo "🚀 Step 5: Starting Agent Zero..."
if $COMPOSE_CMD -f docker-compose.agent-zero.yml up -d; then
    echo "   ✅ Agent Zero started"
else
    echo "   ❌ Failed to start Agent Zero"
    echo "   Trying direct docker run..."
    $USE_SUDO docker run -d -p 50001:80 --name agent-zero --restart unless-stopped agent0ai/agent-zero:latest || true
fi

# Wait a moment
sleep 3

# Step 6: Verify it's running
echo ""
echo "🔍 Step 6: Verifying Agent Zero is running..."
if $USE_SUDO docker ps | grep -q agent-zero; then
    echo "   ✅ Agent Zero is running!"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  ✅ Setup Complete!"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "🌐 Access Agent Zero at: http://localhost:50001"
    echo ""
    echo "📊 Container status:"
    $USE_SUDO docker ps | grep agent-zero
    echo ""
    echo "📝 Useful commands:"
    echo "   View logs:    bash agent_zero_logs.sh"
    echo "   Stop:         bash stop_agent_zero.sh"
    echo "   Restart:      bash start_agent_zero.sh"
    echo ""
    if [ -n "$USE_SUDO" ]; then
        echo "⚠️  Note: You're using sudo for docker commands."
        echo "   After logging out and back in, you won't need sudo."
    fi
else
    echo "   ⚠️  Container may not be running. Check with:"
    echo "      $USE_SUDO docker ps -a | grep agent-zero"
    echo "      $USE_SUDO docker logs agent-zero"
fi

