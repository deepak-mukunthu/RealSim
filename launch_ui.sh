#!/bin/bash
# Simple launcher script for the interactive UI

echo "=================================="
echo "RealSim RL Lab - Desktop App"
echo "=================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "Virtual environment not found."
    echo "Run this first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate venv
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "Virtual environment activated"
echo "Starting interactive UI..."
echo ""

# Run the app
python app.py

echo ""
echo "Thanks for using the simulator!"
