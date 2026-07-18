# Get Started in 3 Minutes

## 1. Activate The Environment

```bash
source venv/bin/activate
```

If you prefer a fresh environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Run The Interactive App

```bash
python app.py
```

The app loads `configs/warehouse_delivery.json`, shows the warehouse map, and lets you start, pause, reset, adjust simulation speed, adjust sensor rays, and toggle Q-learning.

## 3. Watch Automatic RL Training

```bash
python examples/visual_scenario_trainer.py
```

For faster training without a window:

```bash
python examples/visual_scenario_trainer.py --no-render --episodes 50
```

## 4. Create A New World

Copy `configs/warehouse_delivery.json`, then edit robots, targets, zones, and obstacles.

```bash
cp configs/warehouse_delivery.json configs/my_scenario.json
python examples/visual_scenario_trainer.py --scenario configs/my_scenario.json
```

Key files:

- `configs/warehouse_delivery.json`: starter environment.
- `simulations/core/scenario.py`: scenario schema.
- `simulations/warehouse/environment.py`: Gymnasium RL environment.
- `examples/q_learning_agent.py`: tabular Q-learning baseline.
- `app.py`: interactive visual app.
