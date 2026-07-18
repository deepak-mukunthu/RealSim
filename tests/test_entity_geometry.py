import unittest

from simulations.core.entity import Entity, Obstacle, Zone


class EntityGeometryTests(unittest.TestCase):
    def test_circle_robot_collides_with_rectangular_shelf(self):
        robot = Entity((10.0, 10.0), size=0.5)
        shelf = Obstacle((10.6, 10.0), size=(2.0, 4.0), kind="shelf")

        self.assertTrue(robot.collides_with(shelf))

    def test_zone_is_named_non_blocking_context(self):
        zone = Zone((4.0, 6.0), size=(8.0, 3.0), name="Inbound", kind="pickup")

        self.assertEqual(zone.name, "Inbound")
        self.assertEqual(zone.kind, "pickup")
        self.assertEqual(zone.shape, "rect")


if __name__ == "__main__":
    unittest.main()
