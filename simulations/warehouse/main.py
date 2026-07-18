"""Main entry point for warehouse simulation demo."""

from pathlib import Path

import numpy as np
from .environment import WarehouseEnv


def run_demo():
    """Run interactive warehouse simulation demo."""
    print("Warehouse Robot Simulation Demo")
    print("=" * 50)
    print("Watch robots navigate to targets while avoiding obstacles")
    print("Press ESC to quit\n")

    scenario_path = Path(__file__).parent.parent.parent / "configs" / "warehouse_delivery.json"

    # Create environment
    env = WarehouseEnv(
        scenario=scenario_path,
        render_mode='human',
    )

    obs, info = env.reset()

    running = True
    step_count = 0

    while running:
        # This demo sends noisy waypoints toward the configured goal.
        targets = obs.reshape(env.num_robots, 7)[:, 4:6]
        noise = np.random.randn(env.num_robots, 2) * 1.5
        action = targets + noise

        # Take step
        obs, reward, terminated, truncated, info = env.step(action)

        # Render
        env.render()

        # Check if should continue
        if not env.renderer.handle_events():
            running = False

        step_count += 1

        # Reset if done
        if terminated or truncated:
            print(f"\nEpisode finished after {step_count} steps")
            print(f"Robots arrived: {info['robots_arrived']}/{info['total_robots']}")

            # Ask to continue
            print("\nStarting new episode...")
            obs, info = env.reset()
            step_count = 0

    env.close()
    print("\nSimulation closed.")


if __name__ == "__main__":
    run_demo()
