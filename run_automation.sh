#!/bin/bash
# A.V.A. API Keys Automation Runner
# Quick setup script

echo "🚀 A.V.A. API Keys Automation"
echo "=============================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed."
    echo "   Please install Node.js from: https://nodejs.org/"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    echo "   Please install npm (comes with Node.js)"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Run automation
echo "🎯 Starting automation..."
echo "   The browser will open and guide you through each service."
echo "   You may need to complete some steps manually (email verification, CAPTCHA, etc.)"
echo ""
echo "Press Ctrl+C to cancel"
echo ""

node automate_api_setup.js

echo ""
echo "✨ Done! Check the generated files:"
echo "   - api_keys_localStorage.js (for browser)"
echo "   - .env (for Node.js/backend)"
echo "   - api_keys.json (JSON format)"

