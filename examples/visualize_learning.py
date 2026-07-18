"""Backward-compatible visual training entrypoint."""

from examples.visual_scenario_trainer import DEFAULT_SCENARIO, train


if __name__ == "__main__":
    train(
        scenario_path=DEFAULT_SCENARIO,
        episodes=120,
        render=True,
        seed=7,
    )
