#!/bin/bash

# Agent Zero Startup Script
# This script starts Agent Zero using Docker Compose

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🚀 Starting Agent Zero..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    echo "Please run: bash docker_setup.sh"
    exit 1
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon is not running!"
    echo "Please start Docker service: sudo systemctl start docker"
    exit 1
fi

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose is not available!"
    echo "Please install docker-compose or use Docker with compose plugin"
    exit 1
fi

# Pull latest image
echo "📥 Pulling latest Agent Zero image..."
docker pull agent0ai/agent-zero:latest

# Start the container
echo ""
echo "🎬 Starting Agent Zero container..."
$COMPOSE_CMD -f docker-compose.agent-zero.yml up -d

# Wait a moment for container to start
sleep 3

# Check if container is running
if docker ps | grep -q agent-zero; then
    echo ""
    echo "✅ Agent Zero is now running!"
    echo ""
    echo "🌐 Access the web UI at: http://localhost:50001"
    echo ""
    echo "📊 Container status:"
    docker ps | grep agent-zero
    echo ""
    echo "📝 To view logs: docker logs -f agent-zero"
    echo "🛑 To stop: bash stop_agent_zero.sh"
else
    echo ""
    echo "❌ Failed to start Agent Zero container"
    echo "Check logs with: docker logs agent-zero"
    exit 1
fi

