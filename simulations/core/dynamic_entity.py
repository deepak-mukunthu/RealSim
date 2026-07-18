"""Dynamic moving entities for realistic simulations."""

from typing import Tuple, Optional, List
import numpy as np
from .entity import Obstacle


class DynamicObstacle(Obstacle):
    """A moving obstacle that follows a pattern."""

    def __init__(
        self,
        position: Tuple[float, float],
        size: float = 1.0,
        name: str = "Dynamic Obstacle",
        kind: str = "dynamic",
        movement_pattern: str = "linear",
        speed: float = 2.0,
        waypoints: Optional[List[Tuple[float, float]]] = None,
        bounds: Optional[Tuple[float, float]] = None,
    ):
        """
        Args:
            position: Initial (x, y) position
            size: Obstacle radius
            name: Display name
            kind: Type of obstacle
            movement_pattern: "linear", "circular", "patrol", "random"
            speed: Movement speed
            waypoints: List of waypoints for patrol pattern
            bounds: (width, height) of world for boundary checks
        """
        super().__init__(position, size, name, kind)

        self.movement_pattern = movement_pattern
        self.speed = speed
        self.waypoints = waypoints or []
        self.bounds = np.array(bounds) if bounds else None

        # Movement state
        self.current_waypoint = 0
        self.direction = np.array([1.0, 0.0])
        self.angle = 0.0
        self.time = 0.0

        # For circular motion
        self.center = np.array(position, dtype=float)
        self.radius = 10.0

        # For random motion
        self.change_direction_timer = 0.0
        self.change_direction_interval = 3.0

        # Movement history for visualization
        self.trail: List[np.ndarray] = [self.position.copy()]
        self.max_trail_length = 50

    def update(self, dt: float):
        """Update obstacle position based on movement pattern."""
        if not self.active:
            return

        self.time += dt

        if self.movement_pattern == "linear":
            self._update_linear(dt)
        elif self.movement_pattern == "circular":
            self._update_circular(dt)
        elif self.movement_pattern == "patrol":
            self._update_patrol(dt)
        elif self.movement_pattern == "random":
            self._update_random(dt)

        # Record trail
        if len(self.trail) == 0 or np.linalg.norm(self.trail[-1] - self.position) > 0.2:
            self.trail.append(self.position.copy())
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)

    def _update_linear(self, dt: float):
        """Move in a straight line, bouncing off boundaries."""
        self.position += self.direction * self.speed * dt

        # Bounce off boundaries
        if self.bounds is not None:
            if self.position[0] <= self.size or self.position[0] >= self.bounds[0] - self.size:
                self.direction[0] *= -1
                self.position[0] = np.clip(self.position[0], self.size, self.bounds[0] - self.size)

            if self.position[1] <= self.size or self.position[1] >= self.bounds[1] - self.size:
                self.direction[1] *= -1
                self.position[1] = np.clip(self.position[1], self.size, self.bounds[1] - self.size)

    def _update_circular(self, dt: float):
        """Move in a circular pattern."""
        angular_velocity = self.speed / self.radius
        self.angle += angular_velocity * dt

        self.position[0] = self.center[0] + self.radius * np.cos(self.angle)
        self.position[1] = self.center[1] + self.radius * np.sin(self.angle)

        # Update direction for visualization
        self.direction = np.array([
            -np.sin(self.angle),
            np.cos(self.angle)
        ])

    def _update_patrol(self, dt: float):
        """Move between waypoints."""
        if not self.waypoints:
            return

        target = np.array(self.waypoints[self.current_waypoint])
        direction = target - self.position
        distance = np.linalg.norm(direction)

        if distance < 0.5:
            # Reached waypoint, move to next
            self.current_waypoint = (self.current_waypoint + 1) % len(self.waypoints)
            target = np.array(self.waypoints[self.current_waypoint])
            direction = target - self.position
            distance = np.linalg.norm(direction)

        if distance > 0:
            self.direction = direction / distance
            move_distance = min(self.speed * dt, distance)
            self.position += self.direction * move_distance

    def _update_random(self, dt: float):
        """Move in random directions, changing periodically."""
        self.change_direction_timer += dt

        if self.change_direction_timer >= self.change_direction_interval:
            # Change direction
            angle = np.random.uniform(0, 2 * np.pi)
            self.direction = np.array([np.cos(angle), np.sin(angle)])
            self.change_direction_timer = 0.0

        # Move
        self.position += self.direction * self.speed * dt

        # Bounce off boundaries
        if self.bounds is not None:
            if self.position[0] <= self.size or self.position[0] >= self.bounds[0] - self.size:
                self.direction[0] *= -1
                self.position[0] = np.clip(self.position[0], self.size, self.bounds[0] - self.size)

            if self.position[1] <= self.size or self.position[1] >= self.bounds[1] - self.size:
                self.direction[1] *= -1
                self.position[1] = np.clip(self.position[1], self.size, self.bounds[1] - self.size)


class MovingForklift(DynamicObstacle):
    """A forklift that moves through the warehouse."""

    def __init__(self, position: Tuple[float, float], waypoints: List[Tuple[float, float]], bounds: Tuple[float, float]):
        super().__init__(
            position=position,
            size=1.5,
            name="Forklift",
            kind="forklift",
            movement_pattern="patrol",
            speed=8.0,
            waypoints=waypoints,
            bounds=bounds,
        )


class ConveyorBelt(DynamicObstacle):
    """A moving conveyor belt."""

    def __init__(self, position: Tuple[float, float], direction: Tuple[float, float], bounds: Tuple[float, float]):
        super().__init__(
            position=position,
            size=(8.0, 2.0),  # Rectangular
            name="Conveyor",
            kind="conveyor",
            movement_pattern="linear",
            speed=1.5,
            bounds=bounds,
        )
        self.direction = np.array(direction, dtype=float)
        self.direction = self.direction / np.linalg.norm(self.direction)


class RoamingPerson(DynamicObstacle):
    """A person walking randomly through the warehouse."""

    def __init__(self, position: Tuple[float, float], bounds: Tuple[float, float]):
        super().__init__(
            position=position,
            size=0.4,
            name="Worker",
            kind="person",
            movement_pattern="random",
            speed=4.0,
            bounds=bounds,
        )
        self.change_direction_interval = np.random.uniform(2.0, 5.0)
