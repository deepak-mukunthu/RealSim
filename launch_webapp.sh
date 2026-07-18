#!/bin/bash
# Launch the Streamlit web app

echo "=================================="
echo "RealSim RL Lab - Web App"
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

echo ""
echo "Starting web app..."
echo "   Local URL: http://localhost:8501"
echo "   Network URL will be shown below"
echo ""
echo "   Press Ctrl+C to stop"
echo ""

# Launch streamlit
streamlit run streamlit_app.py
