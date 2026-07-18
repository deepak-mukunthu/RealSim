"""Helper method to add to WarehouseEnv for dynamic obstacles."""

def _create_dynamic_obstacles(self):
    """Create dynamic moving obstacles."""
    self.dynamic_obstacles = []

    if not self.enable_dynamic_obstacles:
        return

    # Create different types of dynamic obstacles
    for i in range(self.num_dynamic_obstacles):
        obstacle_type = i % 3

        if obstacle_type == 0:
            # Moving forklift on patrol
            waypoints = [
                (20 + i * 10, 20),
                (20 + i * 10, self.world_size[1] - 20),
                (40 + i * 10, self.world_size[1] - 20),
                (40 + i * 10, 20),
            ]
            forklift = MovingForklift(
                position=waypoints[0],
                waypoints=waypoints,
                bounds=tuple(self.world_size)
            )
            self.dynamic_obstacles.append(forklift)

        elif obstacle_type == 1:
            # Roaming person
            pos = self._sample_clear_position(size=0.4, margin=10.0)
            person = RoamingPerson(
                position=pos,
                bounds=tuple(self.world_size)
            )
            self.dynamic_obstacles.append(person)

        else:
            # Generic circular moving obstacle
            center = np.array([
                self.world_size[0] / 2 + (i - 1) * 15,
                self.world_size[1] / 2
            ])
            obstacle = DynamicObstacle(
                position=center,
                size=1.2,
                name=f"Moving {i+1}",
                kind="dynamic",
                movement_pattern="circular",
                speed=2.5,
                bounds=tuple(self.world_size)
            )
            obstacle.center = center
            obstacle.radius = 8.0 + i * 2
            self.dynamic_obstacles.append(obstacle)
