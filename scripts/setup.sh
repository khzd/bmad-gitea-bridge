#!/bin/bash

# BMad-Gitea-Bridge - Setup Script
# Authors: Khaled Z. & Claude (Anthropic)

set -e

echo "========================================="
echo "  BMad-Gitea-Bridge - Setup"
echo "========================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your credentials"
else
    echo "✅ .env already exists"
fi
echo ""

# Create logs directory
mkdir -p logs
echo "✅ Logs directory ready"
echo ""

# Test installation
echo "🧪 Testing installation..."
python3 src/sync.py --version
echo ""

echo "========================================="
echo "✅ Setup complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env with your credentials"
echo "2. Copy examples/medical-project.yaml to config/projects/"
echo "3. Customize your project config"
echo "4. Run: python src/sync.py --help"
echo ""
