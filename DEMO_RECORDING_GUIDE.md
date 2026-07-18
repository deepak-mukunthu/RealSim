# RealSim Demo Video Recording Guide

This guide helps you create a professional demo video showcasing the key features of RealSim RL Lab.

## 🎬 Quick Start

### Option 1: Automated Screen Recording (Requires Python packages)

```bash
# Install dependencies
pip install opencv-python pillow mss numpy

# Record desktop app demo (30 seconds)
python record_demo.py --app desktop --duration 30

# Record web app demo (30 seconds)
python record_demo.py --app web --duration 30
```

### Option 2: Manual Recording (Recommended for best quality)

Use **QuickTime Player** (Mac), **OBS Studio** (cross-platform), or **Windows Game Bar** (Windows).

---

## 📝 Demo Script (Total: ~2 minutes)

### Scene 1: Desktop App - Initial Exploration (20 seconds)

**What to show:**
- Launch: `python app.py`
- Untrained robots exploring randomly
- Collision detection with obstacles
- Sensor rays visualizing perception
- Real-time physics simulation

**Voiceover/Text overlay:**
> "RealSim RL Lab - Train intelligent agents in realistic simulated environments"

### Scene 2: Web App - Educational Interface (25 seconds)

**What to show:**
- Launch: `streamlit run streamlit_app.py`
- Clean, educational UI with tooltips
- Expand "How RL Works" section
- Show learning phase indicator (🔍 Exploring)
- Live metrics dashboard

**Voiceover/Text overlay:**
> "Interactive web interface makes RL concepts intuitive for learners"

### Scene 3: Dynamic Obstacles (20 seconds)

**What to show:**
- Enable "Dynamic Obstacles" in sidebar
- Set count to 5 obstacles
- Show moving forklifts (patrol pattern)
- Show roaming people (random pattern)
- Show circular conveyor belts
- Robots adapting in real-time

**Voiceover/Text overlay:**
> "Dynamic obstacles create realistic, challenging scenarios"

### Scene 4: Learning Progression (30 seconds)

**What to show:**
- Reset environment and start training
- Phase transitions:
  - 🔍 **Exploring** (random actions) → 10 sec
  - 📚 **Learning** (balancing) → 10 sec
  - 🎯 **Exploiting** (optimal actions) → 10 sec
- Show metrics improving:
  - Success rate increasing
  - Average reward trending upward
  - Episode count incrementing

**Voiceover/Text overlay:**
> "Watch robots progress from random exploration to learned optimal behavior"

### Scene 5: Multi-Agent Coordination (15 seconds)

**What to show:**
- Increase number of robots to 5
- Show coordinated delivery behavior
- Collision avoidance between robots
- Multiple goal zones being serviced

**Voiceover/Text overlay:**
> "Scale to multiple agents with coordination and collision avoidance"

### Scene 6: Code Example (10 seconds)

**What to show:**
- Quick flash of clean code:
```python
from simulations.warehouse.environment import WarehouseEnv

env = WarehouseEnv(enable_dynamic_obstacles=True)
obs, info = env.reset()

for episode in range(100):
    action = agent.act(obs)
    obs, reward, done, _, info = env.step(action)
    agent.learn(obs, action, reward, done)
```

**Voiceover/Text overlay:**
> "Gymnasium-compatible API - easy to integrate with any RL algorithm"

---

## 🎥 Recording Tips

### Before Recording

1. **Clean your desktop** - close unnecessary windows
2. **Set resolution** - 1920x1080 or 1280x720
3. **Disable notifications** - turn on Do Not Disturb mode
4. **Prepare windows** - position app windows in center
5. **Test audio** - if adding voiceover
6. **Run through script** - practice the demo flow

### During Recording

1. **Move cursor smoothly** - no jerky movements
2. **Pause between scenes** - easier to edit later
3. **Keep it concise** - aim for 2-3 minutes total
4. **Show, don't tell** - let the visuals speak
5. **Capture successes** - show robots successfully learning

### Recording Software

#### Mac: QuickTime Player
```bash
# Open QuickTime Player
# File → New Screen Recording
# Select recording region
# Click record button
```

#### Cross-Platform: OBS Studio
1. Download from https://obsproject.com/
2. Add "Window Capture" source
3. Select your app window
4. Click "Start Recording"
5. Export as MP4

#### Windows: Xbox Game Bar
- Press `Win + G`
- Click capture button
- Select recording region

---

## ✂️ Post-Production

### Basic Editing

1. **Trim clips** - remove dead time at start/end
2. **Add title screen** (2-3 seconds):
   ```
   RealSim RL Lab
   Professional Reinforcement Learning Platform
   ```
3. **Add text overlays** - key features/benefits
4. **Add transitions** - smooth fades between scenes
5. **Add end screen** (3 seconds):
   ```
   Learn More:
   github.com/YOUR_USERNAME/RealSim
   ⭐ Star if you find this useful!
   ```

### Tools

- **iMovie** (Mac) - free, simple
- **DaVinci Resolve** (cross-platform) - free, professional
- **Shotcut** (cross-platform) - free, open source
- **Adobe Premiere** - paid, professional

### Optional Enhancements

- **Background music** - use royalty-free tracks from:
  - YouTube Audio Library
  - Incompetech.com
  - Free Music Archive
- **Sound effects** - subtle woosh for transitions
- **Captions** - for accessibility
- **Slow motion** - 0.5x speed for complex interactions

---

## 📤 Export Settings

### For GitHub README
```
Format: MP4 (H.264)
Resolution: 1280x720 (or 1920x1080)
Frame Rate: 30 fps
Bitrate: 5-10 Mbps
File size: < 50 MB (for fast loading)
```

### For YouTube/Vimeo (Optional)
```
Format: MP4 (H.264)
Resolution: 1920x1080
Frame Rate: 60 fps
Bitrate: 15-20 Mbps
```

---

## 📁 Where to Save

```
docs/
├── demo.mp4              # Main demo video
├── demo.gif              # Animated preview (optional)
└── screenshots/
    ├── desktop_app.png
    ├── web_app.png
    └── dynamic_obstacles.png
```

---

## 🔄 Update README

Once you have the demo video:

```markdown
# RealSim RL Lab 🤖

> **Professional Reinforcement Learning Simulation Platform**

![Demo Video](docs/demo.gif)

[📹 Watch Full Demo Video](docs/demo.mp4)

<!-- OR if you upload to YouTube -->
[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
```

---

## 🎯 Key Messages to Convey

1. **Easy to use** - Both visual and code interfaces
2. **Educational** - Designed for learning RL concepts
3. **Realistic** - Dynamic obstacles, physics simulation
4. **Extensible** - Gymnasium-compatible, easy to customize
5. **Professional** - Production-ready for research/demos

---

## ✅ Checklist

Before publishing:

- [ ] Video is under 3 minutes
- [ ] All scenes captured clearly
- [ ] No sensitive information visible
- [ ] Audio is clear (if included)
- [ ] File size is reasonable (< 50 MB)
- [ ] Tested playback on different devices
- [ ] Added to docs/ directory
- [ ] Updated README.md with video link
- [ ] Committed to git repository

---

## 🆘 Troubleshooting

**Video file too large?**
- Reduce resolution to 720p
- Lower bitrate to 5 Mbps
- Trim unnecessary content
- Use GIF for preview, link to YouTube for full video

**Lag during recording?**
- Close other applications
- Reduce app window size
- Lower recording FPS to 24
- Record in shorter segments

**App not visible in recording?**
- Make sure app window is in foreground
- Check screen capture permissions
- Use "Window Capture" instead of "Screen Capture"

---

## 📊 Example Timeline

```
00:00-00:03  Title screen: "RealSim RL Lab"
00:03-00:23  Desktop app - exploration
00:23-00:48  Web app - educational UI
00:48-01:08  Dynamic obstacles feature
01:08-01:38  Learning progression (3 phases)
01:38-01:53  Multi-agent coordination
01:53-02:03  Code example
02:03-02:06  End screen with GitHub link
```

---

## 🚀 Ready to Record!

Start with the automated script or go manual for best quality. Either way, follow the scenes above to create a compelling demo that showcases RealSim's unique features.

**Questions?** Open an issue on GitHub!
