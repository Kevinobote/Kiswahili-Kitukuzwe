#!/bin/bash

# Kiswahili Audio Processing Pipeline - Environment Setup Script

echo "🎯 Setting up Kiswahili Audio Processing Pipeline Environment..."

# Create virtual environment
echo "📦 Creating virtual environment 'sema-deployed'..."
python3 -m venv sema-deployed

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source sema-deployed/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Environment setup complete!"
echo ""
echo "🚀 To start the application:"
echo "1. Activate environment: source sema-deployed/bin/activate"
echo "2. Run server: python main.py"
echo "3. Open browser: http://localhost:8000"
echo ""
echo "📝 Note: First run will download ML models (~2-3GB)"