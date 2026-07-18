#!/usr/bin/env python3
"""
Automated Demo Video Recorder for RealSim RL Lab

Records a demo showing:
1. Desktop app with training visualization
2. Web app with educational features
3. Dynamic obstacles in action
4. Learning progression (exploring -> learning -> exploiting)

Requirements:
    pip install opencv-python pillow mss numpy

Usage:
    python record_demo.py --app desktop  # Record desktop app
    python record_demo.py --app web      # Record web app (opens streamlit)
    python record_demo.py --duration 30  # Record for 30 seconds
"""

import argparse
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime

try:
    import mss
    import cv2
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nInstall with: pip install opencv-python pillow mss numpy")
    sys.exit(1)


class DemoRecorder:
    """Records screen capture for demo video."""

    def __init__(self, output_path: str, fps: int = 30, region=None):
        self.output_path = output_path
        self.fps = fps
        self.region = region
        self.frames = []
        self.sct = mss.mss()

    def add_overlay_text(self, frame: np.ndarray, text: str, position: str = "top") -> np.ndarray:
        """Add text overlay to frame."""
        img = Image.fromarray(frame)
        draw = ImageDraw.Draw(img)

        # Try to load a nice font, fallback to default
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
        except:
            font = ImageFont.load_default()

        # Get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate position
        img_width, img_height = img.size
        if position == "top":
            x = (img_width - text_width) // 2
            y = 30
        elif position == "bottom":
            x = (img_width - text_width) // 2
            y = img_height - text_height - 30
        else:
            x, y = position

        # Draw background rectangle
        padding = 20
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
            fill=(0, 0, 0, 200)
        )

        # Draw text
        draw.text((x, y), text, fill=(255, 255, 255), font=font)

        return np.array(img)

    def record_frame(self, overlay_text: str = None):
        """Capture a single frame."""
        if self.region:
            screenshot = self.sct.grab(self.region)
        else:
            screenshot = self.sct.grab(self.sct.monitors[1])  # Primary monitor

        # Convert to numpy array
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)

        # Add overlay if specified
        if overlay_text:
            frame = self.add_overlay_text(frame, overlay_text)

        self.frames.append(frame)

    def record_duration(self, duration: float, overlay_text: str = None):
        """Record for specified duration."""
        frame_interval = 1.0 / self.fps
        start_time = time.time()
        next_frame_time = start_time

        print(f"Recording for {duration} seconds...")
        while time.time() - start_time < duration:
            current_time = time.time()
            if current_time >= next_frame_time:
                self.record_frame(overlay_text)
                next_frame_time += frame_interval

                # Progress indicator
                elapsed = current_time - start_time
                progress = (elapsed / duration) * 100
                print(f"\rProgress: {progress:.1f}%", end="", flush=True)

            time.sleep(0.001)  # Small sleep to prevent CPU spinning

        print("\nRecording complete!")

    def save_video(self):
        """Save frames as MP4 video."""
        if not self.frames:
            print("No frames recorded!")
            return

        print(f"Saving video to {self.output_path}...")

        height, width = self.frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, self.fps, (width, height))

        for frame in self.frames:
            # Convert RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame_bgr)

        out.release()
        print(f"Video saved: {self.output_path}")
        print(f"Total frames: {len(self.frames)}")
        print(f"Duration: {len(self.frames) / self.fps:.2f} seconds")


def launch_desktop_app():
    """Launch the desktop Pygame app."""
    print("Launching desktop app...")
    return subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def launch_web_app():
    """Launch the Streamlit web app."""
    print("Launching web app...")
    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def create_demo_script():
    """Create a step-by-step demo recording script."""
    script = """
# RealSim Demo Recording Script

## Setup (2 min)
1. Close all unnecessary windows
2. Set screen resolution to 1920x1080 (or 1280x720)
3. Open terminal in project directory
4. Activate virtual environment: source venv/bin/activate

## Scene 1: Desktop App (30 seconds)
1. Run: python app.py
2. Wait for window to open
3. Show: Initial untrained robots wandering
4. Start recording with: python record_demo.py --app desktop --duration 30
5. During recording:
   - Let robots explore for ~10 seconds
   - Show collision detection working
   - Show sensor rays visualizing
   - End with robots starting to learn

## Scene 2: Web App - Overview (30 seconds)
1. Run: streamlit run streamlit_app.py
2. Wait for browser to open (http://localhost:8501)
3. Start recording with: python record_demo.py --app web --duration 30
4. During recording:
   - Show the clean educational UI
   - Hover over tooltips
   - Show "How RL Works" section expanded
   - Show episode counter increasing

## Scene 3: Dynamic Obstacles (30 seconds)
1. In web app sidebar:
   - Enable "Dynamic Obstacles"
   - Set count to 5
2. Start new recording
3. During recording:
   - Show moving forklifts
   - Show roaming people
   - Show robots adapting to dynamic environment

## Scene 4: Learning Progression (45 seconds)
1. Reset environment
2. Start training mode
3. Start recording
4. During recording:
   - Show "🔍 Exploring" phase indicator
   - Wait for transition to "📚 Learning"
   - Wait for transition to "🎯 Exploiting"
   - Show metrics improving (success rate, avg reward)

## Post-Processing
1. Combine clips with: python combine_demo_clips.py
2. Add intro/outro titles
3. Add background music (optional)
4. Export as demo.mp4

## Alternative: Screen Recording Software
Use QuickTime Player (Mac) or OBS Studio (cross-platform):
1. Set recording region to app window
2. Record following the scenes above
3. Export as MP4
4. Place in docs/demo.mp4
"""

    output_path = Path("DEMO_RECORDING_GUIDE.md")
    output_path.write_text(script)
    print(f"Created: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Record RealSim demo video")
    parser.add_argument(
        "--app",
        choices=["desktop", "web"],
        help="Which app to record (desktop or web)"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=30.0,
        help="Recording duration in seconds (default: 30)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: auto-generated)"
    )
    parser.add_argument(
        "--create-guide",
        action="store_true",
        help="Create demo recording guide and exit"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second (default: 30)"
    )

    args = parser.parse_args()

    # Create guide if requested
    if args.create_guide:
        create_demo_script()
        return

    # Generate output filename
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        app_name = args.app if args.app else "screen"
        output_path = f"docs/demo_{app_name}_{timestamp}.mp4"

    # Ensure docs directory exists
    Path("docs").mkdir(exist_ok=True)

    # Launch app if specified
    app_process = None
    if args.app == "desktop":
        app_process = launch_desktop_app()
        print("Waiting for app to start (5 seconds)...")
        time.sleep(5)
    elif args.app == "web":
        app_process = launch_web_app()
        print("Waiting for web app to start (8 seconds)...")
        time.sleep(8)
        print("Browser should open at http://localhost:8501")

    # Start recording
    recorder = DemoRecorder(output_path, fps=args.fps)

    try:
        # Add title overlay for first 3 seconds
        print("\nRecording intro title...")
        recorder.record_duration(3, "RealSim RL Lab - Demo")

        # Record main content
        print("\nRecording main content...")
        recorder.record_duration(args.duration - 3)

        # Save video
        recorder.save_video()

    except KeyboardInterrupt:
        print("\n\nRecording interrupted by user.")
        print("Saving recorded frames...")
        recorder.save_video()

    finally:
        # Clean up
        if app_process:
            print("Stopping app...")
            app_process.terminate()
            app_process.wait(timeout=5)

    print("\n✅ Demo recording complete!")
    print(f"📹 Video saved to: {output_path}")
    print("\nNext steps:")
    print("1. Review the video")
    print("2. Re-record if needed")
    print("3. Update README.md with video link")


if __name__ == "__main__":
    main()
