# Reinforcement Learning Explained

The starter simulation uses Q-learning, a compact reinforcement learning method that is easy to visualize.

## The Loop

```text
Robot observes warehouse state
        |
        v
Q-learning agent chooses waypoint
        |
        v
Environment moves robot and checks collisions
        |
        v
Reward is calculated
        |
        v
Q-table is updated
```

## What The Robot Sees

For each robot, the environment provides:

```text
[x, y, velocity_x, velocity_y, target_x, target_y, needs_goal]
```

The Q-learning baseline turns this into a coarse grid state:

```text
[robot_cell_x, robot_cell_y, target_cell_x, target_cell_y]
```

## What The Agent Does

The agent chooses one short waypoint direction:

- Stay.
- Move horizontally or vertically.
- Move diagonally.

The environment receives that choice as a continuous waypoint, so the same environment can later support neural policies with continuous control.

## Reward

The reward encourages useful robotics behavior:

- Positive reward for getting closer to the target.
- Large bonus when the robot reaches the target.
- Small penalty each step so shorter paths are better.
- Collision penalty when the robot hits blocking geometry.

## Exploration

At first, the agent explores many random moves. Over time, `exploration_rate` decays, and the agent increasingly chooses the best-known Q-table action.

In the visual trainer and app, watch for:

- `Reward`: current episode performance.
- `Avg reward`: recent learning trend.
- `Exploration`: how often the agent still tries random actions.
- `Known states`: how much of the grid-state space the agent has visited.
- `Collisions`: whether the policy is learning to avoid shelves and stations.

## Why Start This Simple?

Q-learning is not the final robotics answer, but it is a good first rung:

- The policy is inspectable.
- Training runs quickly.
- Reward mistakes are easy to spot visually.
- The same environment API can later drive DQN, PPO, SAC, or multi-agent RL.
