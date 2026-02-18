#!/bin/bash
# ============================================
# Railway Auto Deploy Script - Lyra Bot
# ============================================

echo "🚀 Starting Lyra Bot Deployment..."

# Install dependencies
pip install -r requirements.txt

# Ensure persistent folders exist
mkdir -p data
mkdir -p logs

# Check if token.json exists, if not, create empty
if [ ! -f data/token.json ]; then
  echo "{}" > data/token.json
  echo "✅ Created persistent token.json"
fi

# Check queue.json
if [ ! -f data/queue.json ]; then
  echo "[]" > data/queue.json
  echo "✅ Created persistent queue.json"
fi

echo "✅ Setup complete. Starting bot..."
python main.py
