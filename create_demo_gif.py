#!/usr/bin/env python3
"""
Create an animated GIF preview from video or screenshots.

This creates a lightweight GIF suitable for embedding in README.md

Requirements:
    pip install pillow imageio imageio-ffmpeg

Usage:
    # From video
    python create_demo_gif.py --input docs/demo.mp4 --output docs/demo.gif

    # From screenshots
    python create_demo_gif.py --screenshots docs/screenshots/*.png --output docs/demo.gif
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
    import imageio.v3 as iio
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nInstall with: pip install pillow imageio imageio-ffmpeg")
    sys.exit(1)


def resize_image(img: Image.Image, max_width: int = 800) -> Image.Image:
    """Resize image while maintaining aspect ratio."""
    if img.width <= max_width:
        return img

    ratio = max_width / img.width
    new_height = int(img.height * ratio)
    return img.resize((max_width, new_height), Image.Resampling.LANCZOS)


def create_gif_from_video(video_path: str, output_path: str, max_width: int = 800,
                          fps: int = 10, duration: float = None, start_time: float = 0):
    """Create GIF from video file."""
    print(f"Reading video: {video_path}")

    try:
        # Read video
        video = iio.imread(video_path, plugin='pyav')
        total_frames = len(video)
        original_fps = iio.immeta(video_path, plugin='pyav')['fps']

        print(f"Video info: {total_frames} frames at {original_fps} fps")

        # Calculate frame sampling
        frame_skip = int(original_fps / fps)
        start_frame = int(start_time * original_fps)
        end_frame = total_frames if duration is None else int((start_time + duration) * original_fps)

        # Select frames
        selected_frames = []
        for i in range(start_frame, min(end_frame, total_frames), frame_skip):
            frame = Image.fromarray(video[i])
            frame = resize_image(frame, max_width)
            selected_frames.append(frame)

        print(f"Selected {len(selected_frames)} frames for GIF")

        # Save as GIF
        print(f"Saving GIF to: {output_path}")
        selected_frames[0].save(
            output_path,
            save_all=True,
            append_images=selected_frames[1:],
            duration=1000 // fps,  # Duration per frame in ms
            loop=0,  # Loop forever
            optimize=True
        )

        # Report file size
        size_mb = Path(output_path).stat().st_size / (1024 * 1024)
        print(f"✅ GIF created: {output_path}")
        print(f"   Size: {size_mb:.2f} MB")
        print(f"   Frames: {len(selected_frames)}")
        print(f"   FPS: {fps}")

    except Exception as e:
        print(f"❌ Error creating GIF: {e}")
        sys.exit(1)


def create_gif_from_screenshots(screenshot_paths: list, output_path: str,
                                max_width: int = 800, duration_per_frame: int = 1000):
    """Create GIF from screenshot files."""
    print(f"Creating GIF from {len(screenshot_paths)} screenshots")

    frames = []
    for path in sorted(screenshot_paths):
        print(f"  Loading: {path}")
        img = Image.open(path)
        img = resize_image(img, max_width)
        frames.append(img)

    if not frames:
        print("❌ No screenshots found!")
        sys.exit(1)

    print(f"Saving GIF to: {output_path}")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_per_frame,
        loop=0,
        optimize=True
    )

    size_mb = Path(output_path).stat().st_size / (1024 * 1024)
    print(f"✅ GIF created: {output_path}")
    print(f"   Size: {size_mb:.2f} MB")
    print(f"   Frames: {len(frames)}")


def main():
    parser = argparse.ArgumentParser(description="Create animated GIF for demo")
    parser.add_argument("--input", help="Input video file")
    parser.add_argument("--screenshots", nargs="+", help="Input screenshot files")
    parser.add_argument("--output", default="docs/demo.gif", help="Output GIF path")
    parser.add_argument("--max-width", type=int, default=800,
                       help="Maximum width in pixels (default: 800)")
    parser.add_argument("--fps", type=int, default=10,
                       help="Frames per second for GIF (default: 10)")
    parser.add_argument("--duration", type=float,
                       help="Duration in seconds to extract from video")
    parser.add_argument("--start-time", type=float, default=0,
                       help="Start time in seconds (default: 0)")
    parser.add_argument("--frame-duration", type=int, default=1000,
                       help="Duration per frame in ms for screenshot GIFs (default: 1000)")

    args = parser.parse_args()

    # Ensure output directory exists
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    if args.input:
        create_gif_from_video(
            args.input,
            args.output,
            max_width=args.max_width,
            fps=args.fps,
            duration=args.duration,
            start_time=args.start_time
        )
    elif args.screenshots:
        create_gif_from_screenshots(
            args.screenshots,
            args.output,
            max_width=args.max_width,
            duration_per_frame=args.frame_duration
        )
    else:
        print("❌ Error: Must specify either --input (video) or --screenshots")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
