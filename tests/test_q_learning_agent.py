import unittest

import numpy as np

from examples.q_learning_agent import QLearningGridAgent


class QLearningAgentTests(unittest.TestCase):
    def test_q_learning_update_changes_value(self):
        agent = QLearningGridAgent(world_size=(20, 20), seed=3)
        observation = np.array([2, 2, 0, 0, 16, 16, 1], dtype=np.float32)
        next_observation = np.array([5, 2, 0, 0, 16, 16, 1], dtype=np.float32)

        agent.update(observation, action_index=1, reward=1.5, next_observation=next_observation, done=False)

        state = agent.encode_state(observation)
        self.assertGreater(agent.q_table[state][1], 0.0)

    def test_action_waypoint_stays_in_world_bounds(self):
        agent = QLearningGridAgent(world_size=(20, 20), seed=3)
        observation = np.array([1, 1, 0, 0, 16, 16, 1], dtype=np.float32)

        waypoint = agent.action_to_waypoint(observation, action_index=8)

        self.assertGreaterEqual(waypoint[0], 0)
        self.assertGreaterEqual(waypoint[1], 0)


if __name__ == "__main__":
    unittest.main()
