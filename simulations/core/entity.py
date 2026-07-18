"""Base entity classes for all simulation objects."""

from typing import Tuple, Union
import numpy as np


class Entity:
    """Base class for all entities in the simulation."""

    def __init__(self, position: Tuple[float, float], size: float = 1.0):
        """
        Args:
            position: (x, y) coordinates
            size: Radius for circular entities
        """
        self.position = np.array(position, dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.size = size
        self.active = True

    def update(self, dt: float):
        """Update entity state. Override in subclasses."""
        if self.active:
            self.position += self.velocity * dt

    def distance_to(self, other: 'Entity') -> float:
        """Calculate distance to another entity."""
        return np.linalg.norm(self.position - other.position)

    def collides_with(self, other: 'Entity') -> bool:
        """Check collision with another entity."""
        if getattr(self, "shape", "circle") == "rect" and getattr(other, "shape", "circle") == "rect":
            return _rectangles_overlap(self, other)

        if getattr(self, "shape", "circle") == "rect":
            return _circle_collides_with_rect(other, self)

        if getattr(other, "shape", "circle") == "rect":
            return _circle_collides_with_rect(self, other)

        return self.distance_to(other) < (self.size + other.size)


class Obstacle(Entity):
    """Static obstacle in the environment."""

    def __init__(
        self,
        position: Tuple[float, float],
        size: Union[float, Tuple[float, float]] = 1.0,
        name: str = "Obstacle",
        kind: str = "obstacle",
        shape: str = "circle",
    ):
        if isinstance(size, (list, tuple, np.ndarray)):
            width, height = float(size[0]), float(size[1])
            radius = max(width, height) / 2.0
            shape = "rect"
        else:
            width = height = float(size) * 2.0
            radius = float(size)

        super().__init__(position, radius)
        self.velocity = np.array([0.0, 0.0])
        self.name = name
        self.kind = kind
        self.shape = shape
        self.width = width
        self.height = height

    def update(self, dt: float):
        """Obstacles don't update."""
        pass


class Zone(Entity):
    """A non-blocking semantic area such as pickup, dropoff, or charging."""

    def __init__(
        self,
        position: Tuple[float, float],
        size: Tuple[float, float],
        name: str,
        kind: str = "zone",
    ):
        width, height = float(size[0]), float(size[1])
        super().__init__(position, max(width, height) / 2.0)
        self.name = name
        self.kind = kind
        self.shape = "rect"
        self.width = width
        self.height = height

    def update(self, dt: float):
        """Zones are visual context and do not move."""
        pass


def _rect_bounds(entity: Entity) -> Tuple[float, float, float, float]:
    half_width = getattr(entity, "width", entity.size * 2.0) / 2.0
    half_height = getattr(entity, "height", entity.size * 2.0) / 2.0
    left = entity.position[0] - half_width
    right = entity.position[0] + half_width
    top = entity.position[1] - half_height
    bottom = entity.position[1] + half_height
    return left, top, right, bottom


def _rectangles_overlap(first: Entity, second: Entity) -> bool:
    first_left, first_top, first_right, first_bottom = _rect_bounds(first)
    second_left, second_top, second_right, second_bottom = _rect_bounds(second)
    return (
        first_left < second_right
        and first_right > second_left
        and first_top < second_bottom
        and first_bottom > second_top
    )


def _circle_collides_with_rect(circle: Entity, rect: Entity) -> bool:
    left, top, right, bottom = _rect_bounds(rect)
    closest = np.array(
        [
            np.clip(circle.position[0], left, right),
            np.clip(circle.position[1], top, bottom),
        ]
    )
    return np.linalg.norm(circle.position - closest) < circle.size
