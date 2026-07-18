# Documentation

This directory contains documentation, demo videos, and screenshots for RealSim RL Lab.

## 📁 Contents

### Demo Media

- **demo.mp4** - Full demo video (2-3 minutes)
- **demo.gif** - Animated preview for README
- **screenshots/** - High-quality screenshots of key features

### Guides

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture overview
- **[RL_EXPLAINED.md](RL_EXPLAINED.md)** - Reinforcement learning concepts explained
- **[UI_GUIDE.md](UI_GUIDE.md)** - User interface guide

## 🎬 Creating Demo Video

See the [Demo Recording Guide](../DEMO_RECORDING_GUIDE.md) in the root directory for detailed instructions on recording and editing demo videos.

### Quick Recording

```bash
# Automated screen recording (requires: pip install opencv-python pillow mss numpy)
python record_demo.py --app web --duration 30

# Or use screen recording software
# Mac: QuickTime Player → New Screen Recording
# Windows: Win+G (Xbox Game Bar)
# Cross-platform: OBS Studio
```

### Converting Video to GIF

```bash
# Install dependencies
pip install pillow imageio imageio-ffmpeg

# Create GIF from video
python create_demo_gif.py --input docs/demo.mp4 --output docs/demo.gif --max-width 800 --fps 10
```

## 📸 Screenshots

Place screenshots in the `screenshots/` directory with descriptive names:

```
screenshots/
├── desktop_app.png          # Desktop Pygame interface
├── web_app.png              # Streamlit web interface
├── learning_phases.png      # Exploring → Learning → Exploiting
├── dynamic_obstacles.png    # Moving forklifts and people
├── metrics_dashboard.png    # Performance charts
└── code_example.png         # Code snippet
```

### Taking Screenshots

**Mac:**
- `Cmd + Shift + 4` → Select region
- `Cmd + Shift + 4` → `Space` → Click window

**Windows:**
- `Win + Shift + S` → Select region
- `Win + PrtScn` → Full screen

**Linux:**
- `gnome-screenshot -a` → Select region

## 📋 Screenshot Checklist

When capturing screenshots for documentation:

- [ ] Use consistent resolution (1920x1080 or 1280x720)
- [ ] Disable desktop notifications
- [ ] Close irrelevant windows
- [ ] Center the application window
- [ ] Show interesting state (robots learning, obstacles moving)
- [ ] Use high-quality PNG format
- [ ] Annotate if needed (arrows, highlights)

## 🎨 Branding

### Logo
If you create a logo, place it here:
- `logo.png` - Full logo with text (transparent background)
- `logo_icon.png` - Icon only (square, transparent)

### Color Scheme
```
Primary:   #2E86DE (Blue)
Success:   #26DE81 (Green)
Warning:   #FFC048 (Orange)
Danger:    #FC5C65 (Red)
Text:      #2F3542 (Dark Gray)
Background: #F8F9FA (Light Gray)
```

## 📝 Adding New Documentation

1. Create markdown file in this directory
2. Follow existing formatting style
3. Add links in main README.md
4. Include code examples where relevant
5. Add screenshots/diagrams if helpful

## 🔗 External Links

If you publish tutorials or blog posts about RealSim, add them here:

- [Your Blog Post Title](https://example.com) - Brief description
- [Tutorial: Getting Started with RealSim](https://example.com) - Step-by-step guide
- [Video: Building RL Agents](https://youtube.com) - YouTube tutorial

## 📊 Demo Scenes Reference

Key moments to capture in demos:

1. **Initial Exploration** - Untrained robots moving randomly
2. **Collision Detection** - Robots bouncing off obstacles
3. **Sensor Visualization** - Rays showing perception
4. **Dynamic Obstacles** - Moving forklifts and people
5. **Learning Phases** - 🔍 Exploring → 📚 Learning → 🎯 Exploiting
6. **Metrics Dashboard** - Charts showing improvement
7. **Multi-Agent** - Multiple robots coordinating
8. **Code Example** - Clean API usage

## 🆘 Help

If you need help creating demo content:

1. Check [DEMO_RECORDING_GUIDE.md](../DEMO_RECORDING_GUIDE.md)
2. Look at existing examples in this directory
3. Open an issue on GitHub
4. Reach out to the community

---

**Pro tip:** Keep demo videos under 3 minutes and GIFs under 5MB for fast loading!
