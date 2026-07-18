# Architecture

RealSim RL Lab is split into scenario data, simulation runtime, rendering, and agents.

```text
JSON Scenario
     |
     v
ScenarioSpec ---> WarehouseEnv <---- RL Agent
                    |   ^
                    v   |
              Physics + Reward
                    |
                    v
                 Renderer
```

## Scenario Layer

`simulations/core/scenario.py` defines portable environment descriptions:

- `RobotSpec`: start position, speed, acceleration, sensor range.
- `TargetSpec`: assigned goal locations.
- `ObstacleSpec`: blocking shelves, stations, pillars, or walls.
- `ZoneSpec`: visible non-blocking areas such as pickup, dropoff, staging, or charging.

The first scenario lives in `configs/warehouse_delivery.json`.

## Simulation Runtime

`WarehouseEnv` in `simulations/warehouse/environment.py` follows the Gymnasium API:

```python
observation, info = env.reset()
next_observation, reward, terminated, truncated, info = env.step(action)
```

Observation per robot:

```text
[x, y, vx, vy, target_x, target_y, needs_goal]
```

Action per robot:

```text
[waypoint_x, waypoint_y]
```

Rewards combine progress, arrival bonus, small time cost, and collision penalties.

## Rendering

`simulations/core/renderer.py` draws:

- Rectangular shelves and stations.
- Translucent semantic zones.
- Target rings and labels.
- Robot body, heading, path trail, and sensor rays.
- Compact simulation and training panels.

The same renderer is used by the standalone environment and the interactive `app.py`.

## RL Baseline

`examples/q_learning_agent.py` implements tabular Q-learning:

- Discretizes the robot and goal into grid cells.
- Chooses a short waypoint with epsilon-greedy exploration.
- Updates the Q-table from reward and the next state's best value.

This baseline is intentionally small. It makes the learning loop visible before moving to neural policies.

## Extension Path

- Add richer scenario fields for dynamic actors and materials.
- Add lidar noise, camera-like observations, or occupancy grids.
- Replace Q-learning with DQN, PPO, SAC, or multi-agent RL.
- Add a ROS 2 bridge and export logs for sim-to-real validation.
- Move physics-heavy scenarios to PyBullet, MuJoCo, Isaac Sim, or another 3D engine.
