# Demo Assets Placeholder

This file serves as a placeholder until you record your demo video and create assets.

## 📹 Missing Assets

The following files need to be created:

- [ ] **demo.mp4** - Main demo video (2-3 minutes)
- [ ] **demo.gif** - Animated preview for README (< 5 MB)
- [ ] **screenshots/** - Key feature screenshots

## 🎬 How to Create

### Quick Start

```bash
# Run interactive setup
./setup_demo.sh
```

### Manual Steps

1. **Record video** - See [DEMO_QUICK_START.md](../DEMO_QUICK_START.md)
2. **Convert to GIF**:
   ```bash
   python create_demo_gif.py --input docs/demo.mp4 --output docs/demo.gif
   ```
3. **Take screenshots** - Save to `docs/screenshots/`
4. **Update README** - Add links to assets
5. **Delete this file** - Once assets are created

## 📚 Full Guide

See [DEMO_RECORDING_GUIDE.md](../DEMO_RECORDING_GUIDE.md) for comprehensive instructions.

## 🎯 What Makes a Good Demo

1. **Show the journey** - Random exploration → Learned behavior
2. **Highlight features** - Dynamic obstacles, multi-agent, metrics
3. **Keep it short** - 2-3 minutes maximum
4. **High quality** - 1080p or 720p, smooth recording
5. **Educational** - Show what makes your project unique

## ✅ When You're Done

1. Delete this PLACEHOLDER.md file
2. Verify assets work in README.md
3. Commit and push to GitHub
4. Your project now has a professional demo! 🎉

---

**Quick recording:** `python record_demo.py --app web --duration 30`
