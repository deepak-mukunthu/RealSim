"""Pygame-based visualization renderer."""

from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pygame

from .entity import Entity, Obstacle, Zone


class Renderer:
    """Handles all visualization using Pygame."""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        scale: float = 8.0,
        screen: Optional[pygame.Surface] = None,
    ):
        """
        Args:
            width: Window width in pixels
            height: Window height in pixels
            scale: Pixels per simulation unit
        """
        pygame.init()
        self.width = width
        self.height = height
        self.scale = scale
        self.screen = screen or pygame.display.set_mode((width, height))
        if screen is None:
            pygame.display.set_caption("AI Robotics Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 19)
        self.title_font = pygame.font.Font(None, 28)

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.FLOOR = (245, 247, 250)
        self.GRID = (218, 225, 235)
        self.GRAY = (103, 116, 136)
        self.DARK = (29, 41, 57)
        self.RED = (211, 47, 47)
        self.GREEN = (31, 142, 75)
        self.BLUE = (37, 99, 235)
        self.YELLOW = (234, 179, 8)
        self.AMBER = (217, 119, 6)
        self.CYAN = (8, 145, 178)
        self.PANEL = (255, 255, 255)

        self.kind_colors = {
            "shelf": (84, 98, 122),
            "wall": (51, 65, 85),
            "station": (110, 91, 211),
            "charger": (8, 145, 178),
            "obstacle": self.GRAY,
        }

        self.zone_colors = {
            "pickup": (8, 145, 178),
            "dropoff": (31, 142, 75),
            "charging": (234, 179, 8),
            "staging": (110, 91, 211),
            "zone": (100, 116, 139),
        }

    def world_to_screen(self, position: np.ndarray) -> tuple:
        """Convert world coordinates to screen pixels."""
        x = int(position[0] * self.scale)
        y = int(position[1] * self.scale)
        return (x, y)

    def world_rect_to_screen(self, position: np.ndarray, size: Tuple[float, float]) -> pygame.Rect:
        """Convert a centered world rectangle to screen pixels."""
        width = int(size[0] * self.scale)
        height = int(size[1] * self.scale)
        center_x, center_y = self.world_to_screen(position)
        return pygame.Rect(center_x - width // 2, center_y - height // 2, width, height)

    def clear(self):
        """Clear the screen."""
        self.screen.fill(self.FLOOR)

    def draw_entity(self, entity: Entity, color: Optional[tuple] = None):
        """Draw a single entity."""
        if not entity.active:
            return

        if isinstance(entity, Obstacle):
            self.draw_obstacle(entity, color=color)
            return

        if isinstance(entity, Zone):
            self.draw_zone(entity)
            return

        pos = self.world_to_screen(entity.position)
        radius = int(entity.size * self.scale)

        if color is None:
            if isinstance(entity, Obstacle):
                color = self.GRAY
            else:
                color = self.BLUE

        pygame.draw.circle(self.screen, color, pos, radius)

        # Draw velocity vector if moving
        if np.linalg.norm(entity.velocity) > 0.1:
            end_pos = self.world_to_screen(
                entity.position + entity.velocity * 0.5
            )
            pygame.draw.line(self.screen, self.RED, pos, end_pos, 2)

    def draw_entities(self, entities: List[Entity]):
        """Draw all entities."""
        for entity in entities:
            self.draw_entity(entity)

    def draw_text(self, text: str, position: tuple, color: tuple = None):
        """Draw text at screen position."""
        if color is None:
            color = self.BLACK
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, position)

    def draw_small_text(self, text: str, position: tuple, color: tuple = None):
        """Draw compact text at screen position."""
        if color is None:
            color = self.DARK
        surface = self.small_font.render(text, True, color)
        self.screen.blit(surface, position)

    def draw_grid(self, cell_size: float = 10.0):
        """Draw a grid for reference."""
        spacing = max(1, int(cell_size * self.scale))
        for x in range(0, self.width, spacing):
            pygame.draw.line(self.screen, self.GRID, (x, 0), (x, self.height))
        for y in range(0, self.height, spacing):
            pygame.draw.line(self.screen, self.GRID, (0, y), (self.width, y))

    def draw_obstacle(self, obstacle: Obstacle, color: Optional[tuple] = None):
        """Draw a blocking obstacle with a shape-aware glyph."""
        color = color or self.kind_colors.get(obstacle.kind, self.GRAY)
        if obstacle.shape == "rect":
            rect = self.world_rect_to_screen(obstacle.position, (obstacle.width, obstacle.height))
            pygame.draw.rect(self.screen, color, rect, border_radius=3)
            pygame.draw.rect(self.screen, self.DARK, rect, width=1, border_radius=3)
            self._draw_centered_label(obstacle.name, rect.center, self.WHITE)
            return

        pos = self.world_to_screen(obstacle.position)
        radius = int(obstacle.size * self.scale)
        pygame.draw.circle(self.screen, color, pos, radius)
        pygame.draw.circle(self.screen, self.DARK, pos, radius, width=1)

    def draw_zone(self, zone: Zone):
        """Draw a non-blocking semantic zone."""
        color = self.zone_colors.get(zone.kind, self.zone_colors["zone"])
        rect = self.world_rect_to_screen(zone.position, (zone.width, zone.height))
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        surface.fill((*color, 42))
        self.screen.blit(surface, rect.topleft)
        pygame.draw.rect(self.screen, color, rect, width=2, border_radius=3)
        self._draw_centered_label(zone.name, rect.center, color)

    def draw_target(self, position: np.ndarray, name: str = "Goal", color: tuple = None):
        """Draw a target marker."""
        color = color or self.GREEN
        pos = self.world_to_screen(position)
        pygame.draw.circle(self.screen, color, pos, 11, 3)
        pygame.draw.circle(self.screen, color, pos, 3)
        self.draw_small_text(name, (pos[0] + 12, pos[1] - 8), color)

    def draw_robot(self, robot: Entity, color: tuple = None, show_sensor: bool = True):
        """Draw a robot with trail, body, heading, and optional sensor radius."""
        color = color or self.BLUE
        pos = self.world_to_screen(robot.position)

        if getattr(robot, "trail", None) and len(robot.trail) > 1:
            points = [self.world_to_screen(point) for point in robot.trail[-90:]]
            pygame.draw.lines(self.screen, (83, 145, 245), False, points, 2)

        if show_sensor and getattr(robot, "sensor_range", 0) > 0:
            sensor_radius = int(robot.sensor_range * self.scale)
            sensor_surface = pygame.Surface((sensor_radius * 2 + 2, sensor_radius * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(sensor_surface, (*self.BLUE, 18), (sensor_radius + 1, sensor_radius + 1), sensor_radius)
            self.screen.blit(sensor_surface, (pos[0] - sensor_radius - 1, pos[1] - sensor_radius - 1))

        radius = max(5, int(robot.size * self.scale))
        pygame.draw.circle(self.screen, color, pos, radius)
        pygame.draw.circle(self.screen, self.WHITE, pos, max(2, radius // 3))

        velocity = getattr(robot, "velocity", np.array([0.0, 0.0]))
        if np.linalg.norm(velocity) > 0.1:
            end_pos = self.world_to_screen(robot.position + velocity * 0.65)
            pygame.draw.line(self.screen, self.RED, pos, end_pos, 3)

        label = getattr(robot, "name", f"R{getattr(robot, 'robot_id', 0) + 1}")
        self.draw_small_text(label, (pos[0] + 9, pos[1] + 8), self.DARK)

    def draw_sensor_rays(self, robot: Entity, readings: Sequence[float], max_range: float):
        """Draw coarse range sensor rays around a robot."""
        if readings is None or len(readings) == 0:
            return
        origin = self.world_to_screen(robot.position)
        for index, distance in enumerate(readings):
            angle = (index / len(readings)) * np.pi * 2.0
            endpoint = robot.position + np.array([np.cos(angle), np.sin(angle)]) * distance
            screen_endpoint = self.world_to_screen(endpoint)
            color = self.CYAN if distance > max_range * 0.35 else self.RED
            pygame.draw.line(self.screen, color, origin, screen_endpoint, 1)

    def draw_status_panel(self, title: str, lines: Iterable[Tuple[str, str]], position: tuple = (10, 10)):
        """Draw a compact information panel."""
        line_items = list(lines)
        width = 280
        height = 42 + len(line_items) * 23
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((*self.PANEL, 232))
        self.screen.blit(panel, position)
        rect = pygame.Rect(position[0], position[1], width, height)
        pygame.draw.rect(self.screen, (148, 163, 184), rect, width=1, border_radius=4)

        title_surface = self.title_font.render(title, True, self.DARK)
        self.screen.blit(title_surface, (position[0] + 12, position[1] + 10))

        y = position[1] + 38
        for label, value in line_items:
            self.draw_small_text(f"{label}:", (position[0] + 12, y), (71, 85, 105))
            self.draw_small_text(str(value), (position[0] + 142, y), self.DARK)
            y += 23

    def _draw_centered_label(self, text: str, center: tuple, color: tuple):
        if not text:
            return
        surface = self.small_font.render(text, True, color)
        rect = surface.get_rect(center=center)
        self.screen.blit(surface, rect)

    def update(self):
        """Update the display."""
        pygame.display.flip()

    def tick(self, fps: int = 60) -> float:
        """
        Limit framerate and return dt in seconds.

        Returns:
            Time since last frame in seconds
        """
        return self.clock.tick(fps) / 1000.0

    def handle_events(self) -> bool:
        """
        Handle pygame events.

        Returns:
            False if user wants to quit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def close(self):
        """Clean up pygame."""
        pygame.quit()
