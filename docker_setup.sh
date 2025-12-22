#!/bin/bash

# Docker Installation and Setup Script for Agent-Zero (Zorin Linux)
# Run this script with: bash docker_setup.sh

echo "=== Docker Installation and Agent-Zero Setup for Zorin Linux ==="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing Docker..."
    echo "You will be prompted for your password."
    sudo apt update
    sudo apt install -y docker.io
    
    # Start Docker service
    echo "Starting Docker service..."
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Add current user to docker group (to run without sudo)
    echo "Adding user to docker group..."
    sudo usermod -aG docker $USER
    echo ""
    echo "⚠️  IMPORTANT: You need to log out and log back in (or restart) for group changes to take effect."
    echo "   After logging back in, you can run Docker commands without sudo."
    echo ""
    echo "Alternatively, you can use 'newgrp docker' to apply changes in current session,"
    echo "or run docker commands with 'sudo' prefix."
    echo ""
else
    echo "Docker is already installed."
    echo ""
fi

# Pull the Agent-Zero Docker image
echo "Pulling Agent-Zero Docker image..."
if docker pull agent0ai/agent-zero:latest; then
    echo "✅ Image pulled successfully"
else
    echo "❌ Failed to pull image. You may need to use 'sudo docker pull'"
    echo "Or log out and log back in after being added to docker group."
    exit 1
fi

echo ""
echo "✅ Docker setup complete!"
echo ""
echo "Next steps:"
echo "1. If you were added to docker group, LOG OUT and LOG BACK IN"
echo "2. Then run: bash start_agent_zero.sh"
echo ""
echo "Or start manually with:"
echo "   docker-compose -f docker-compose.agent-zero.yml up -d"
echo ""
echo "Access Agent Zero at: http://localhost:50001"

