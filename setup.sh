#!/bin/bash

# Upstox MCP Setup Script
# Works on macOS and Linux

set -e

echo "🚀 Initializing Upstox MCP Setup..."

# 1. Create Virtual Environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists."
fi

# 2. Activate Virtual Environment and Install Dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -e .

# 3. Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "📄 Creating .env from .env.example..."
        cp .env.example .env
        echo "⚠️  Action Required: Update your credentials in the .env file!"
    else
        echo "⚠️  Warning: .env.example not found. Please create a .env file manually."
    fi
else
    echo "✅ .env file already exists."
fi

# 4. Verify Installation
echo "🔍 Verifying installation..."
if command -v upstox-mcp &> /dev/null; then
    VERSION=$(upstox-mcp --version)
    echo "✅ Success! $VERSION is installed and ready."
else
    echo "❌ Error: upstox-mcp command not found. Please ensure your PATH is set correctly."
    exit 1
fi

echo "---"
echo "🎉 Setup Complete!"
echo "To start using the server, run:"
echo "source venv/bin/activate"
echo "upstox-mcp"
