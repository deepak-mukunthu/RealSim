# Features

## Configurable Environments

- JSON scenarios for world size, robots, targets, zones, and obstacles.
- Rectangular shelves/stations and circular obstacles.
- Non-blocking semantic zones such as inbound, packing, and charging.

## Reinforcement Learning

- Gymnasium-compatible `WarehouseEnv`.
- Tabular Q-learning starter agent in `examples/q_learning_agent.py`.
- Reward shaping for progress, arrival, time cost, and collisions.
- Headless and visual training modes.

## Visualization

- Pygame desktop renderer with robot trails, sensor rays, labeled targets, shelves, zones, and live stats.
- Static browser UI with canvas simulation, build mode, JSON editing, and no dependency install.
- Streamlit browser view with scenario map, reward chart, and controls.
- Matplotlib scenario rendering for shareable web demos.

## Entry Points

```bash
python app.py
open web/index.html
python examples/visual_scenario_trainer.py
python examples/visual_scenario_trainer.py --no-render --episodes 30
streamlit run streamlit_app.py
```

## Current Starter Scenario

`configs/warehouse_delivery.json` models a single autonomous cart moving through a warehouse aisle from inbound staging to a packing lane.

## Roadmap

- Multi-robot task allocation.
- Neural policies with DQN, PPO, or SAC.
- Sensor noise, occlusion, and occupancy-grid observations.
- Dynamic actors such as people, forklifts, and doors.
- ROS 2 bridge and sim-to-real validation tools.
