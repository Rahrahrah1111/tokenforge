#!/bin/bash

# Agent Zero Logs Viewer
# This script shows the logs from the Agent Zero container

echo "📝 Agent Zero Logs (Press Ctrl+C to exit)"
echo ""

# Check if container is running
if ! docker ps | grep -q agent-zero; then
    echo "❌ Agent Zero container is not running"
    echo "Start it with: bash start_agent_zero.sh"
    exit 1
fi

# Show logs
docker logs -f agent-zero

