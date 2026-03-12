#!/bin/bash

# Quick Modal Deployment Script for Kiswahili Audio Pipeline
# Uses existing conda environment: audio_ml
# Usage: ./deploy_modal.sh

set -e

echo "🚀 Kiswahili Audio Pipeline - Modal Deployment"
echo "=============================================="
echo ""

# Activate conda environment
echo "🔧 Activating conda environment: audio_ml"
source ~/anaconda3/etc/profile.d/conda.sh
conda activate audio_ml

echo "✅ Conda environment activated"
echo ""

# Verify Modal is available
if ! command -v modal &> /dev/null; then
    echo "❌ Modal not found in audio_ml environment"
    echo "Installing Modal..."
    pip install modal
else
    echo "✅ Modal is available"
fi

echo ""

# Check Modal authentication
echo "🔐 Checking Modal authentication..."
if modal profile current &> /dev/null; then
    PROFILE=$(modal profile current)
    echo "✅ Modal authentication verified (Profile: $PROFILE)"
else
    echo "❌ Modal authentication failed"
    echo "Please run: modal setup"
    exit 1
fi

echo ""
echo "🚀 Deploying to Modal..."
echo ""

# Deploy the app
modal deploy modal_app.py

echo ""
echo "=============================================="
echo "✅ Deployment Complete!"
echo ""
echo "📱 Your app is now live!"
echo ""
echo "To get your app URL, run:"
echo "   conda activate audio_ml"
echo "   modal app list"
echo ""
echo "📊 View logs:"
echo "   modal app logs kiswahili-audio-pipeline --follow"
echo ""
echo "💰 Check usage:"
echo "   modal profile current"
echo ""
echo "🔄 Update deployment:"
echo "   conda activate audio_ml"
echo "   modal deploy modal_app.py"
echo ""
echo "🎉 Happy researching!"
echo "=============================================="