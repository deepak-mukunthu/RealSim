# Interactive App Guide

Run:

```bash
source venv/bin/activate
python app.py
```

## Main Controls

- `Start`: runs the current scenario.
- `Pause`: pauses or resumes.
- `Reset`: reloads the scenario and clears training stats.
- `New Episode`: starts a fresh episode without closing the app.
- `Training`: toggles Q-learning on or off.

## Sliders

- `Steps/frame`: increases simulation speed by advancing multiple environment steps per rendered frame.
- `Sensor Rays`: changes the number of visible range-sensor rays and resets the episode.

## Visual Elements

- Blue robot: active robot.
- Green robot: robot has reached its assigned goal.
- Green ring: target.
- Dark blocks: shelves, pillars, or stations.
- Tinted rectangles: semantic zones such as inbound, packing, or charging.
- Blue trail: recent robot path.
- Thin rays: coarse sensor readings.

## Training Stats

When training is enabled, the panel shows:

- `Avg Reward`: recent reward trend.
- `Best`: best episode reward so far.
- `Exploration`: current epsilon-greedy randomness.
- `Known States`: number of grid states in the Q-table.

## Custom Scenarios

The app loads `configs/warehouse_delivery.json` by default. To use another file, change `DEFAULT_SCENARIO` in `app.py`, or run training directly:

```bash
python examples/visual_scenario_trainer.py --scenario configs/my_scenario.json
```
