from pathlib import Path
import unittest

from simulations.core.scenario import ScenarioSpec


class ScenarioTests(unittest.TestCase):
    def test_loads_starter_scenario(self):
        scenario = ScenarioSpec.from_json(Path("configs/warehouse_delivery.json"))

        self.assertEqual(scenario.name, "Warehouse Delivery Starter")
        self.assertEqual(scenario.world_size, (82.0, 56.0))
        self.assertEqual(scenario.robots[0].name, "Cart A")
        self.assertEqual(scenario.targets[0].name, "Packing Lane")
        self.assertEqual(scenario.obstacles[0].shape, "rect")
        self.assertEqual(scenario.zones[0].kind, "pickup")


if __name__ == "__main__":
    unittest.main()
