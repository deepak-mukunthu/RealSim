"""Legacy hand-crafted policy used for simple interface demonstrations."""

import numpy as np
from typing import List, Tuple


class SimpleRLAgent:
    """
    A simple rule-based policy that demonstrates the environment interface.
    Use QLearningGridAgent for the starter reinforcement learning baseline.
    """

    def __init__(self, num_robots: int, learning_rate: float = 0.01):
        self.num_robots = num_robots
        self.learning_rate = learning_rate

        # Simple policy: gradually learn to move towards targets
        self.exploration_rate = 1.0  # Start with full exploration
        self.min_exploration = 0.05
        self.exploration_decay = 0.995

        # Track performance
        self.episode_rewards: List[float] = []
        self.episode_steps: List[int] = []

    def select_action(self, observation: np.ndarray) -> np.ndarray:
        """
        Select actions based on current policy.

        Args:
            observation: [x, y, vx, vy, target_x, target_y, needs_goal] * num_robots

        Returns:
            actions: [target_x, target_y] * num_robots
        """
        obs = observation.reshape(self.num_robots, 7)
        actions = []

        for i in range(self.num_robots):
            robot_obs = obs[i]
            current_pos = robot_obs[0:2]
            target_pos = robot_obs[4:6]

            # Exploration vs exploitation
            if np.random.random() < self.exploration_rate:
                # Explore: add noise to target
                noise = np.random.randn(2) * 10.0
                action = target_pos + noise
            else:
                # Exploit: move directly to target
                action = target_pos

            actions.append(action)

        return np.array(actions).flatten()

    def update(self, reward: float, done: bool):
        """Update policy based on reward (simplified for demo)."""
        # Decay exploration rate
        if done:
            self.exploration_rate = max(
                self.min_exploration,
                self.exploration_rate * self.exploration_decay
            )

    def log_episode(self, total_reward: float, steps: int):
        """Log episode statistics."""
        self.episode_rewards.append(total_reward)
        self.episode_steps.append(steps)

    def get_stats(self) -> dict:
        """Get current training statistics."""
        if not self.episode_rewards:
            return {
                'episodes': 0,
                'avg_reward': 0.0,
                'best_reward': 0.0,
                'avg_steps': 0.0,
                'exploration_rate': self.exploration_rate
            }

        recent = min(10, len(self.episode_rewards))
        return {
            'episodes': len(self.episode_rewards),
            'avg_reward': np.mean(self.episode_rewards[-recent:]),
            'best_reward': np.max(self.episode_rewards),
            'avg_steps': np.mean(self.episode_steps[-recent:]),
            'exploration_rate': self.exploration_rate
        }
