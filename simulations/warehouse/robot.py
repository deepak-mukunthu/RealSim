"""Robot agent for warehouse simulation."""

import numpy as np
from typing import Optional, Tuple
from ..core.entity import Entity


class Robot(Entity):
    """A mobile robot agent in the warehouse."""

    def __init__(
        self,
        position: Tuple[float, float],
        robot_id: int = 0,
        name: Optional[str] = None,
        max_speed: float = 5.0,
        acceleration: float = 10.0,
        sensor_range: float = 8.0,
    ):
        """
        Args:
            position: Starting (x, y) coordinates
            robot_id: Unique identifier for this robot
        """
        super().__init__(position, size=0.5)
        self.robot_id = robot_id
        self.name = name or f"Robot {robot_id + 1}"
        self.target: Optional[np.ndarray] = None
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.sensor_range = sensor_range
        self.arrived_threshold = 0.5
        self.trail = [self.position.copy()]
        self.max_trail_points = 180

    def set_target(self, target: Tuple[float, float]):
        """Set a new target destination."""
        self.target = np.array(target, dtype=float)

    def has_target(self) -> bool:
        """Check if robot has an active target."""
        return self.target is not None

    def has_arrived(self) -> bool:
        """Check if robot has reached its target."""
        if self.target is None:
            return True
        distance = np.linalg.norm(self.position - self.target)
        return distance < self.arrived_threshold

    def update(self, dt: float):
        """Update robot movement towards target."""
        if not self.active or self.target is None:
            return

        # Check if arrived
        if self.has_arrived():
            self.velocity *= 0.9  # Slow down
            if np.linalg.norm(self.velocity) < 0.1:
                self.velocity = np.array([0.0, 0.0])
                self.target = None
            return

        # Simple seek behavior - move towards target
        direction = self.target - self.position
        distance = np.linalg.norm(direction)

        if distance > 0:
            direction = direction / distance  # Normalize

            # Desired velocity
            desired_velocity = direction * self.max_speed

            # Steering force
            steering = desired_velocity - self.velocity
            steering_magnitude = np.linalg.norm(steering)

            if steering_magnitude > self.acceleration * dt:
                steering = steering / steering_magnitude * self.acceleration * dt

            self.velocity += steering

        # Update position
        super().update(dt)
        self._record_trail()

    def get_state(self) -> dict:
        """Get robot state for observation."""
        return {
            'id': self.robot_id,
            'name': self.name,
            'position': self.position.copy(),
            'velocity': self.velocity.copy(),
            'target': self.target.copy() if self.target is not None else None,
            'has_arrived': self.has_arrived()
        }

    def _record_trail(self):
        """Keep a short path history for visual debugging."""
        if not self.trail or np.linalg.norm(self.trail[-1] - self.position) > 0.05:
            self.trail.append(self.position.copy())
        if len(self.trail) > self.max_trail_points:
            self.trail.pop(0)
