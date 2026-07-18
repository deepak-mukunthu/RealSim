"""Train the starter scenario without visualization."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.visual_scenario_trainer import DEFAULT_SCENARIO, train


if __name__ == "__main__":
    train(
        scenario_path=DEFAULT_SCENARIO,
        episodes=150,
        render=False,
        seed=11,
    )
