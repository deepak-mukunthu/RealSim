# 🎬 Demo Quick Start

The fastest way to create a demo video for your GitHub repo.

## Option 1: Automated (Python Script)

```bash
# Install dependencies
pip install opencv-python pillow mss imageio imageio-ffmpeg

# Run interactive setup
./setup_demo.sh

# Or record directly
python record_demo.py --app web --duration 30
```

## Option 2: Manual (Best Quality)

### 1. Screen Recording Software

**macOS - QuickTime Player** (Built-in, Free)
```bash
1. Open QuickTime Player
2. File → New Screen Recording
3. Click Options → Choose Microphone (optional)
4. Click record button → Select region
5. Start your app
6. Stop recording when done
7. File → Export As → 1080p
8. Save to docs/demo.mp4
```

**Windows - Xbox Game Bar** (Built-in, Free)
```
1. Press Win + G
2. Click Capture button (camera icon)
3. Click Record button
4. Start your app
5. Press Win + Alt + R to stop
6. Video saved to Videos/Captures/
7. Move to docs/demo.mp4
```

**Cross-Platform - OBS Studio** (Free, Professional)
```
1. Download from https://obsproject.com/
2. Add "Window Capture" source
3. Select your app window
4. Click "Start Recording"
5. Export as MP4 to docs/demo.mp4
```

### 2. What to Record (2 minutes total)

**Scene 1: Opening** (5 sec)
- Launch app
- Show initial screen

**Scene 2: Basic Features** (30 sec)
- Robots exploring
- Sensor rays visible
- Collision detection

**Scene 3: Dynamic Obstacles** (20 sec)
- Toggle on in sidebar
- Show moving forklifts/people

**Scene 4: Learning** (45 sec)
- Start training
- Show phase progression: 🔍→📚→🎯
- Show metrics improving

**Scene 5: Multi-Agent** (15 sec)
- Increase robot count
- Show coordination

**Scene 6: Closing** (5 sec)
- Show GitHub link or project name

### 3. Convert to GIF

```bash
# Create preview GIF for README
python create_demo_gif.py \
  --input docs/demo.mp4 \
  --output docs/demo.gif \
  --max-width 800 \
  --fps 10
```

## Option 3: Screenshots Only

If you don't have time for video:

```bash
# Take 5-6 key screenshots and save to docs/screenshots/

# macOS: Cmd+Shift+4 → Select area
# Windows: Win+Shift+S → Select area

# Required shots:
1. web_app_overview.png - Main interface
2. learning_phases.png - Phase indicator
3. dynamic_obstacles.png - Moving obstacles
4. metrics_dashboard.png - Charts
5. desktop_app.png - Pygame version
```

Create GIF from screenshots:
```bash
python create_demo_gif.py \
  --screenshots docs/screenshots/*.png \
  --output docs/demo.gif \
  --frame-duration 1500
```

## 📋 Pre-Recording Checklist

- [ ] Close unnecessary apps
- [ ] Enable Do Not Disturb mode
- [ ] Set resolution to 1920x1080 or 1280x720
- [ ] Center app window
- [ ] Test record 5 seconds to verify it works
- [ ] Have interesting scenario loaded (robots learning, obstacles enabled)

## ✅ Post-Recording Steps

1. **Review the video** - Make sure it looks good
2. **Trim if needed** - Remove dead time at start/end
3. **Create GIF** - For README preview
4. **Update README** - Add video/GIF links
5. **Commit to git**:
   ```bash
   git add docs/demo.* docs/screenshots/
   git commit -m "Add demo video and screenshots"
   ```

## 🎯 Target Specs

**Video:**
- Format: MP4 (H.264)
- Resolution: 1280x720 or 1920x1080
- Duration: 1-3 minutes
- File size: < 50 MB
- FPS: 30

**GIF:**
- Format: GIF
- Resolution: 800px width
- FPS: 10
- File size: < 5 MB
- Loop: Forever

## 🆘 Troubleshooting

**"Permission denied" on macOS?**
```
System Settings → Privacy & Security → Screen Recording
→ Enable for Terminal/Python
```

**Video file too large?**
```bash
# Reduce size with ffmpeg
ffmpeg -i docs/demo.mp4 -vcodec h264 -b:v 5000k docs/demo_compressed.mp4
```

**GIF too large?**
```bash
# Reduce resolution/fps
python create_demo_gif.py --input docs/demo.mp4 --output docs/demo.gif --max-width 600 --fps 8
```

## 🚀 Ready?

```bash
# Start recording!
./setup_demo.sh

# Or jump straight to it
python record_demo.py --app web --duration 30
```

---

**Done?** Update [README_GITHUB.md](README_GITHUB.md) and push to GitHub! 🎉
