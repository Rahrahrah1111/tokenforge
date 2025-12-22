#!/bin/bash

# Agent Zero Stop Script
# This script stops the Agent Zero container

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🛑 Stopping Agent Zero..."

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "Using docker stop directly..."
    docker stop agent-zero 2>/dev/null || echo "Container not running"
    exit 0
fi

# Stop the container
$COMPOSE_CMD -f docker-compose.agent-zero.yml down

echo ""
echo "✅ Agent Zero has been stopped"
echo ""
echo "To start again: bash start_agent_zero.sh"

