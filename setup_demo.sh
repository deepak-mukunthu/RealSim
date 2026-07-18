#!/bin/bash

# Demo Setup Script for RealSim RL Lab
# Helps you quickly record demo video and create assets

set -e

echo "🎬 RealSim Demo Setup"
echo "===================="
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "   Run: source venv/bin/activate"
    echo ""
    exit 1
fi

# Check for recording dependencies
echo "📦 Checking dependencies..."
if python -c "import mss, cv2, PIL, imageio" 2>/dev/null; then
    echo "✅ Recording dependencies installed"
else
    echo "⚠️  Some dependencies missing"
    echo "   Installing: opencv-python pillow mss imageio imageio-ffmpeg"
    pip install opencv-python pillow mss imageio imageio-ffmpeg
    echo "✅ Dependencies installed"
fi
echo ""

# Create directories
echo "📁 Creating directories..."
mkdir -p docs/screenshots
echo "✅ Directories ready"
echo ""

# Check if demo files exist
if [ -f "docs/demo.mp4" ]; then
    echo "📹 Existing demo video found: docs/demo.mp4"
else
    echo "📹 No demo video found yet"
fi

if [ -f "docs/demo.gif" ]; then
    echo "🖼️  Existing demo GIF found: docs/demo.gif"
else
    echo "🖼️  No demo GIF found yet"
fi
echo ""

# Menu
echo "What would you like to do?"
echo ""
echo "1) Create demo recording guide"
echo "2) Record desktop app demo (30 sec)"
echo "3) Record web app demo (30 sec)"
echo "4) Convert existing video to GIF"
echo "5) Take screenshots manually"
echo "6) View recording tips"
echo "7) Exit"
echo ""
read -p "Enter choice [1-7]: " choice

case $choice in
    1)
        python record_demo.py --create-guide
        echo ""
        echo "✅ Created: DEMO_RECORDING_GUIDE.md"
        echo "   Read it for detailed recording instructions"
        ;;
    2)
        echo ""
        echo "Starting desktop app recording in 5 seconds..."
        echo "Get ready to interact with the app!"
        sleep 2
        python record_demo.py --app desktop --duration 30
        ;;
    3)
        echo ""
        echo "Starting web app recording in 8 seconds..."
        echo "Browser will open automatically"
        sleep 2
        python record_demo.py --app web --duration 30
        ;;
    4)
        if [ -f "docs/demo.mp4" ]; then
            echo ""
            echo "Converting demo.mp4 to demo.gif..."
            python create_demo_gif.py --input docs/demo.mp4 --output docs/demo.gif --max-width 800 --fps 10
        else
            echo ""
            echo "❌ No demo.mp4 found in docs/"
            echo "   Record a video first (option 2 or 3)"
        fi
        ;;
    5)
        echo ""
        echo "Screenshot Instructions:"
        echo ""
        echo "macOS:"
        echo "  • Cmd+Shift+4 → Select area"
        echo "  • Cmd+Shift+4 → Space → Click window"
        echo ""
        echo "Windows:"
        echo "  • Win+Shift+S → Select area"
        echo "  • Win+PrtScn → Full screen"
        echo ""
        echo "Save screenshots to: docs/screenshots/"
        echo ""
        echo "Recommended shots:"
        echo "  1. Desktop app with robots learning"
        echo "  2. Web app with educational UI"
        echo "  3. Dynamic obstacles in action"
        echo "  4. Learning phase indicator"
        echo "  5. Metrics dashboard"
        echo ""
        read -p "Press Enter when done..."
        ;;
    6)
        echo ""
        echo "🎥 Recording Tips:"
        echo ""
        echo "Before Recording:"
        echo "  • Close unnecessary windows"
        echo "  • Disable notifications (Do Not Disturb)"
        echo "  • Set screen resolution to 1920x1080 or 1280x720"
        echo "  • Position app window in center"
        echo ""
        echo "During Recording:"
        echo "  • Move cursor smoothly"
        echo "  • Let robots learn for 20-30 seconds"
        echo "  • Show dynamic obstacles toggle"
        echo "  • Highlight learning phase transitions"
        echo ""
        echo "After Recording:"
        echo "  • Trim dead time at start/end"
        echo "  • Add title overlay if desired"
        echo "  • Convert to GIF for README preview"
        echo "  • Keep video under 3 minutes"
        echo "  • Keep GIF under 5 MB"
        echo ""
        echo "Alternative: Use QuickTime (Mac) or OBS Studio for manual recording"
        echo ""
        read -p "Press Enter to continue..."
        ;;
    7)
        echo "Goodbye! 👋"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Done!"
echo ""
echo "Next steps:"
echo "  1. Review the recorded video/screenshots"
echo "  2. Re-record if needed"
echo "  3. Convert video to GIF: python create_demo_gif.py --input docs/demo.mp4 --output docs/demo.gif"
echo "  4. Update README.md with the demo assets"
echo "  5. Commit and push to GitHub"
echo ""
