"""Train a Q-learning robot in a user-defined scenario."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.q_learning_agent import QLearningGridAgent
from simulations.warehouse.environment import WarehouseEnv


DEFAULT_SCENARIO = Path(__file__).parent.parent / "configs" / "warehouse_delivery.json"


def train(
    scenario_path: Path = DEFAULT_SCENARIO,
    episodes: int = 120,
    render: bool = True,
    seed: int = 7,
):
    """Train a simple Q-learning policy in a configured warehouse."""
    env = WarehouseEnv(
        scenario=scenario_path,
        render_mode="human" if render else None,
        sensor_ray_count=16,
    )
    agent = QLearningGridAgent(
        world_size=tuple(env.world_size),
        grid_size=4.0,
        waypoint_stride=5.5,
        seed=seed,
    )

    print("=" * 72)
    print("CONFIGURABLE RL SIMULATION")
    print("=" * 72)
    print(f"Scenario: {scenario_path}")
    print(f"Episodes: {episodes}")
    print(f"Visual: {render}")
    print("Press ESC in the simulation window to stop early.\n")

    for episode in range(1, episodes + 1):
        observation, info = env.reset(seed=seed + episode)
        total_reward = 0.0
        total_collisions = 0
        done = False

        while not done:
            action_index, action = agent.select_action(observation)
            next_observation, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            agent.update(observation, action_index, reward, next_observation, done)
            observation = next_observation
            total_reward += reward
            total_collisions += info["collisions"]

            if render:
                env.render()
                _draw_training_overlay(env, agent, episode, total_reward)
                if env.renderer:
                    env.renderer.update()
                    if not env.renderer.handle_events():
                        env.close()
                        print("\nTraining stopped by user.")
                        return agent

        agent.finish_episode(total_reward, info["step"], total_collisions)
        stats = agent.get_stats()
        print(
            f"Episode {episode:03d} | "
            f"reward {total_reward:7.2f} | "
            f"steps {info['step']:3d} | "
            f"arrived {info['robots_arrived']}/{info['total_robots']} | "
            f"epsilon {stats['exploration_rate']:.2%} | "
            f"states {stats['known_states']}"
        )

    env.close()
    print("\nTraining complete.")
    print(_format_final_stats(agent.get_stats()))
    return agent


def _draw_training_overlay(env: WarehouseEnv, agent: QLearningGridAgent, episode: int, reward: float):
    if not env.renderer:
        return

    stats = agent.get_stats()
    env.renderer.draw_status_panel(
        "Q-Learning",
        [
            ("Episode", str(episode)),
            ("Reward", f"{reward:.2f}"),
            ("Avg reward", f"{stats['avg_reward']:.2f}"),
            ("Best reward", f"{stats['best_reward']:.2f}"),
            ("Exploration", f"{stats['exploration_rate']:.1%}"),
            ("Known states", str(stats["known_states"])),
        ],
        position=(env.renderer.width - 295, 10),
    )


def _format_final_stats(stats: dict) -> str:
    return (
        f"Episodes: {stats['episodes']} | "
        f"Best reward: {stats['best_reward']:.2f} | "
        f"Avg reward: {stats['avg_reward']:.2f} | "
        f"Avg steps: {stats['avg_steps']:.1f} | "
        f"Avg collisions: {stats['avg_collisions']:.1f}"
    )


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", type=Path, default=DEFAULT_SCENARIO)
    parser.add_argument("--episodes", type=int, default=120)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--no-render", action="store_true", help="Train without opening a pygame window")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train(
        scenario_path=args.scenario,
        episodes=args.episodes,
        render=not args.no_render,
        seed=args.seed,
    )
