"""Small tabular Q-learning agent for the warehouse scenario."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np


Action = Tuple[int, int]
State = Tuple[int, int, int, int]


class QLearningGridAgent:
    """
    A minimal Q-learning baseline for one robot.

    The agent discretizes the robot and goal positions into grid cells, chooses
    a short waypoint action, and updates a Q-table from observed reward.
    """

    ACTIONS: Tuple[Action, ...] = (
        (0, 0),
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    )

    def __init__(
        self,
        world_size: Tuple[float, float],
        grid_size: float = 4.0,
        waypoint_stride: float = 4.0,
        learning_rate: float = 0.18,
        discount: float = 0.94,
        exploration_rate: float = 1.0,
        min_exploration: float = 0.08,
        exploration_decay: float = 0.92,
        goal_bias: float = 0.65,
        seed: int | None = None,
    ):
        self.world_size = np.array(world_size, dtype=float)
        self.grid_size = float(grid_size)
        self.waypoint_stride = float(waypoint_stride)
        self.learning_rate = learning_rate
        self.discount = discount
        self.exploration_rate = exploration_rate
        self.min_exploration = min_exploration
        self.exploration_decay = exploration_decay
        self.goal_bias = goal_bias
        self.rng = np.random.default_rng(seed)

        self.q_table: Dict[State, np.ndarray] = defaultdict(
            lambda: np.zeros(len(self.ACTIONS), dtype=float)
        )
        self.episode_rewards: List[float] = []
        self.episode_steps: List[int] = []
        self.collision_counts: List[int] = []

    def select_action(self, observation: np.ndarray) -> Tuple[int, np.ndarray]:
        """Return an action index and continuous waypoint action."""
        state = self.encode_state(observation)
        if self.rng.random() < self.exploration_rate:
            if self.rng.random() < self.goal_bias:
                action_index = self._goal_directed_action(observation)
            else:
                action_index = int(self.rng.integers(len(self.ACTIONS)))
        else:
            values = self.q_table[state]
            if float(np.max(values)) <= 0.0:
                action_index = self._goal_directed_action(observation)
            else:
                action_index = int(np.argmax(values))

        return action_index, self.action_to_waypoint(observation, action_index)

    def encode_state(self, observation: np.ndarray) -> State:
        """Discretize [x, y, vx, vy, goal_x, goal_y, needs_goal]."""
        robot = np.asarray(observation, dtype=float).reshape(-1, 7)[0]
        position_cell = np.floor(robot[0:2] / self.grid_size).astype(int)
        target_cell = np.floor(robot[4:6] / self.grid_size).astype(int)
        return (
            int(position_cell[0]),
            int(position_cell[1]),
            int(target_cell[0]),
            int(target_cell[1]),
        )

    def action_to_waypoint(self, observation: np.ndarray, action_index: int) -> np.ndarray:
        """Convert a discrete move into the environment's waypoint action."""
        robot = np.asarray(observation, dtype=float).reshape(-1, 7)[0]
        direction = np.array(self.ACTIONS[action_index], dtype=float)
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)

        distance_to_goal = np.linalg.norm(robot[4:6] - robot[0:2])
        if distance_to_goal <= self.waypoint_stride:
            waypoint = robot[4:6]
        else:
            waypoint = robot[0:2] + direction * self.waypoint_stride
        waypoint = np.clip(waypoint, [0.0, 0.0], self.world_size)
        return waypoint.astype(np.float32)

    def _goal_directed_action(self, observation: np.ndarray) -> int:
        """Choose the discrete direction that most directly reduces goal distance."""
        robot = np.asarray(observation, dtype=float).reshape(-1, 7)[0]
        delta = robot[4:6] - robot[0:2]
        direction = (
            int(np.sign(delta[0])) if abs(delta[0]) > self.grid_size * 0.5 else 0,
            int(np.sign(delta[1])) if abs(delta[1]) > self.grid_size * 0.5 else 0,
        )
        return self.ACTIONS.index(direction)

    def update(
        self,
        observation: np.ndarray,
        action_index: int,
        reward: float,
        next_observation: np.ndarray,
        done: bool,
    ):
        """Apply the Q-learning value update."""
        state = self.encode_state(observation)
        next_state = self.encode_state(next_observation)

        old_value = self.q_table[state][action_index]
        next_best = 0.0 if done else float(np.max(self.q_table[next_state]))
        target = reward + self.discount * next_best
        self.q_table[state][action_index] = old_value + self.learning_rate * (target - old_value)

    def finish_episode(self, total_reward: float, steps: int, collisions: int):
        """Log stats and reduce random exploration."""
        self.episode_rewards.append(total_reward)
        self.episode_steps.append(steps)
        self.collision_counts.append(collisions)
        self.exploration_rate = max(
            self.min_exploration,
            self.exploration_rate * self.exploration_decay,
        )

    def get_stats(self) -> dict:
        """Return compact training stats for logs and visual panels."""
        if not self.episode_rewards:
            return {
                "episodes": 0,
                "avg_reward": 0.0,
                "best_reward": 0.0,
                "avg_steps": 0.0,
                "avg_collisions": 0.0,
                "exploration_rate": self.exploration_rate,
                "known_states": len(self.q_table),
            }

        window = min(20, len(self.episode_rewards))
        return {
            "episodes": len(self.episode_rewards),
            "avg_reward": float(np.mean(self.episode_rewards[-window:])),
            "best_reward": float(np.max(self.episode_rewards)),
            "avg_steps": float(np.mean(self.episode_steps[-window:])),
            "avg_collisions": float(np.mean(self.collision_counts[-window:])),
            "exploration_rate": self.exploration_rate,
            "known_states": len(self.q_table),
        }
