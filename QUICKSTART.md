# Quick Start

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run The Visual RL Demo

```bash
python3 examples/visual_scenario_trainer.py
```

You will see:

- A warehouse map with shelves, pickup/dropoff zones, and a charging area.
- A blue robot learning to reach the green target.
- A trail showing where the robot has moved.
- Sensor rays showing nearby walls and obstacles.
- Live Q-learning stats: reward, exploration, best reward, and known states.

Press `ESC` to stop.

## Run The Apps

```bash
python3 app.py
open web/index.html
streamlit run streamlit_app.py
```

## Train Without A Window

```bash
python3 examples/train_simple.py
```

Or run fewer episodes:

```bash
python3 examples/visual_scenario_trainer.py --no-render --episodes 25
```

## Create Your Own Environment

Copy [configs/warehouse_delivery.json](configs/warehouse_delivery.json), then edit:

- `robots` for robot start state and movement limits.
- `targets` for delivery goals.
- `zones` for semantic areas that should be visible but not blocking.
- `obstacles` for shelves, machinery, walls, pillars, or other blocked space.

Run your scenario:

```bash
python3 examples/visual_scenario_trainer.py --scenario configs/my_scenario.json
```

## How The Reward Works

The robot receives:

- Positive reward for getting closer to its assigned target.
- A large bonus when it reaches the target.
- A small time penalty each step.
- A collision penalty when it contacts shelves or obstacles.

That reward shaping keeps the first simulation easy to understand while leaving room for advanced robotics-style experiments later.
