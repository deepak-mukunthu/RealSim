"""Simple physics engine for 2D simulation."""

import numpy as np
from typing import List
from .entity import Entity


class PhysicsEngine:
    """Handles physics updates and collision detection."""

    def __init__(self, bounds: tuple = (100, 100)):
        """
        Args:
            bounds: (width, height) of simulation space
        """
        self.bounds = np.array(bounds)
        self.max_speed = 10.0

    def update(self, entities: List[Entity], dt: float):
        """Update all entities with physics."""
        for entity in entities:
            if not entity.active:
                continue

            # Clamp velocity
            speed = np.linalg.norm(entity.velocity)
            if speed > self.max_speed:
                entity.velocity = entity.velocity / speed * self.max_speed

            # Update position
            entity.update(dt)

            # Keep within bounds
            entity.position = np.clip(
                entity.position,
                [entity.size, entity.size],
                self.bounds - entity.size
            )

    def check_collisions(self, entities: List[Entity]) -> List[tuple]:
        """
        Check for collisions between entities.

        Returns:
            List of (entity1, entity2) collision pairs
        """
        collisions = []
        for i, e1 in enumerate(entities):
            for e2 in entities[i+1:]:
                if e1.active and e2.active and e1.collides_with(e2):
                    collisions.append((e1, e2))
        return collisions
