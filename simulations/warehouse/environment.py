"""Gymnasium-compatible warehouse environment for RL training."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from ..core.entity import Obstacle, Zone
from ..core.physics import PhysicsEngine
from ..core.scenario import ScenarioSpec
from ..core.dynamic_entity import DynamicObstacle, MovingForklift, RoamingPerson
from .robot import Robot


class WarehouseEnv(gym.Env):
    """
    Warehouse robot coordination environment.

    Observation:
        For each robot: [x, y, vx, vy, target_x, target_y, needs_goal]

    Action:
        For each robot: [waypoint_x, waypoint_y]
    """

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}

    def __init__(
        self,
        num_robots: int = 3,
        world_size: Tuple[float, float] = (100, 75),
        num_obstacles: int = 10,
        max_steps: int = 1000,
        render_mode: Optional[str] = None,
        scenario: Optional[Union[ScenarioSpec, str, Path]] = None,
        sensor_ray_count: int = 12,
        include_sensor_readings: bool = False,
        enable_dynamic_obstacles: bool = False,
        num_dynamic_obstacles: int = 3,
    ):
        super().__init__()

        self.enable_dynamic_obstacles = enable_dynamic_obstacles
        self.num_dynamic_obstacles = num_dynamic_obstacles
        self.dynamic_obstacles: List[DynamicObstacle] = []

        self.scenario = self._load_scenario(scenario)
        if self.scenario:
            world_size = self.scenario.world_size
            if self.scenario.robots:
                num_robots = len(self.scenario.robots)
            num_obstacles = len(self.scenario.obstacles)
            max_steps = int(self.scenario.metadata.get("max_steps", max_steps))

        self.num_robots = num_robots
        self.world_size = np.array(world_size, dtype=float)
        self.num_obstacles = num_obstacles
        self.max_steps = max_steps
        self.render_mode = render_mode
        self.sensor_ray_count = sensor_ray_count
        self.include_sensor_readings = include_sensor_readings

        self.physics = PhysicsEngine(bounds=world_size)
        self.dt = 1.0 / 60.0

        self.robots: List[Robot] = []
        self.obstacles: List[Obstacle] = []
        self.zones: List[Zone] = []
        self.targets: List[np.ndarray] = []
        self.target_names: List[str] = []

        obs_dim = num_robots * 7
        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(obs_dim,),
            dtype=np.float32,
        )

        self.action_space = spaces.Box(
            low=np.zeros(num_robots * 2, dtype=np.float32),
            high=np.tile(self.world_size.astype(np.float32), num_robots),
            dtype=np.float32,
        )

        self.step_count = 0
        self.renderer = None
        self._rng = np.random.default_rng()
        self._previous_distances = np.zeros(self.num_robots, dtype=float)
        self._arrival_awarded = [False] * self.num_robots
        self._last_collision_count = 0

    def _load_scenario(self, scenario: Optional[Union[ScenarioSpec, str, Path]]) -> Optional[ScenarioSpec]:
        if scenario is None or isinstance(scenario, ScenarioSpec):
            return scenario
        return ScenarioSpec.from_json(scenario)

    def _create_obstacles(self):
        """Create blocking geometry in the warehouse."""
        self.obstacles = []

        if self.scenario:
            for spec in self.scenario.obstacles:
                self.obstacles.append(
                    Obstacle(
                        spec.position,
                        spec.size,
                        name=spec.name,
                        kind=spec.kind,
                        shape=spec.shape,
                    )
                )
            return

        for index in range(self.num_obstacles):
            pos = self._sample_clear_position(size=2.0, margin=10.0)
            size = float(self._rng.uniform(1.0, 3.0))
            self.obstacles.append(Obstacle(pos, size, name=f"Obstacle {index + 1}"))

    def _create_zones(self):
        """Create non-blocking semantic zones."""
        self.zones = []
        if not self.scenario:
            return

        for spec in self.scenario.zones:
            self.zones.append(
                Zone(
                    spec.position,
                    spec.size,
                    name=spec.name,
                    kind=spec.kind,
                )
            )

    def _create_robots(self):
        """Create robots from scenario or random positions."""
        self.robots = []

        if self.scenario and self.scenario.robots:
            for index, spec in enumerate(self.scenario.robots):
                self.robots.append(
                    Robot(
                        spec.position,
                        robot_id=index,
                        name=spec.name,
                        max_speed=spec.max_speed,
                        acceleration=spec.acceleration,
                        sensor_range=spec.sensor_range,
                    )
                )
            return

        for index in range(self.num_robots):
            pos = self._sample_clear_position(size=0.5, margin=5.0)
            self.robots.append(Robot(pos, robot_id=index))

    def _generate_targets(self):
        """Generate target positions for each robot."""
        self.targets = []
        self.target_names = []

        if self.scenario and self.scenario.targets:
            for spec in self.scenario.targets[: self.num_robots]:
                self.targets.append(np.array(spec.position, dtype=float))
                self.target_names.append(spec.name)

        while len(self.targets) < self.num_robots:
            self.targets.append(self._sample_clear_position(size=0.5, margin=5.0))
            self.target_names.append(f"Goal {len(self.targets)}")

    def _sample_clear_position(self, size: float, margin: float) -> np.ndarray:
        """Sample a point that does not overlap existing blocking objects."""
        low = np.array([margin, margin], dtype=float)
        high = self.world_size - margin

        for _ in range(500):
            pos = self._rng.uniform(low, high)
            probe = Robot(pos, robot_id=-1)
            probe.size = size
            if all(not probe.collides_with(obstacle) for obstacle in self.obstacles):
                if all(np.linalg.norm(pos - robot.position) > robot.size + size + 1.0 for robot in self.robots):
                    return pos

        return self._rng.uniform([size, size], self.world_size - size)

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        """Reset the environment."""
        super().reset(seed=seed)
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        self._create_obstacles()
        self._create_zones()
        self._create_robots()
        self._generate_targets()
        self._create_dynamic_obstacles()

        self.step_count = 0
        self._last_collision_count = 0
        self._arrival_awarded = [False] * self.num_robots
        self._previous_distances = self._goal_distances()

        observation = self._get_observation()
        info = self._get_info()

        return observation, info

    def _get_observation(self) -> np.ndarray:
        """Get current observation."""
        obs = []
        for index, robot in enumerate(self.robots):
            state = robot.get_state()
            target = self.targets[index]
            obs.extend(
                [
                    state["position"][0],
                    state["position"][1],
                    state["velocity"][0],
                    state["velocity"][1],
                    target[0],
                    target[1],
                    0.0 if self._arrival_awarded[index] else 1.0,
                ]
            )
        return np.array(obs, dtype=np.float32)

    def _get_info(self) -> dict:
        """Get additional info for dashboards and diagnostics."""
        distances = self._goal_distances() if self.robots and self.targets else np.array([])
        info = {
            "step": self.step_count,
            "robots_arrived": sum(self._arrival_awarded),
            "total_robots": self.num_robots,
            "collisions": self._last_collision_count,
            "avg_goal_distance": float(np.mean(distances)) if len(distances) else 0.0,
            "scenario": self.scenario.name if self.scenario else "Random Warehouse",
        }
        if self.include_sensor_readings:
            info["sensor_readings"] = [
                self.get_sensor_readings(index).tolist()
                for index in range(len(self.robots))
            ]
        return info

    def step(self, action: np.ndarray):
        """Execute one step of the simulation."""
        self.step_count += 1

        action = np.asarray(action, dtype=float).reshape(self.num_robots, 2)
        action = np.clip(action, [0.0, 0.0], self.world_size)

        for index, robot in enumerate(self.robots):
            if not self._arrival_awarded[index]:
                robot.set_target(action[index])

        # Update dynamic obstacles
        for dyn_obs in self.dynamic_obstacles:
            dyn_obs.update(self.dt)

        previous_positions = [robot.position.copy() for robot in self.robots]
        all_entities = self.robots + self.obstacles + self.dynamic_obstacles
        self.physics.update(all_entities, self.dt)

        collisions = self.physics.check_collisions(all_entities)
        robot_collisions = [
            pair for pair in collisions if any(isinstance(entity, Robot) for entity in pair)
        ]
        self._last_collision_count = len(robot_collisions)
        self._resolve_robot_collisions(robot_collisions, previous_positions)

        distances = self._goal_distances()
        reward = self._calculate_reward(distances, self._last_collision_count)

        self._previous_distances = distances
        terminated = all(self._arrival_awarded)
        truncated = self.step_count >= self.max_steps

        observation = self._get_observation()
        info = self._get_info()

        return observation, reward, terminated, truncated, info

    def _resolve_robot_collisions(self, collisions: List[tuple], previous_positions: List[np.ndarray]):
        """Move robots back slightly after contact so obstacles remain readable."""
        for first, second in collisions:
            for entity in (first, second):
                if isinstance(entity, Robot) and entity.robot_id >= 0:
                    entity.position = previous_positions[entity.robot_id]
                    entity.velocity *= -0.15

    def _calculate_reward(self, distances: np.ndarray, collision_count: int) -> float:
        """Calculate shaped reward based on progress, arrivals, and contacts."""
        reward = -0.02 * self.num_robots

        for index, distance in enumerate(distances):
            progress = self._previous_distances[index] - distance
            reward += progress * 0.8

            if distance < self.robots[index].arrived_threshold:
                if not self._arrival_awarded[index]:
                    reward += 25.0
                self._arrival_awarded[index] = True
                self.robots[index].set_target(self.robots[index].position)
            else:
                reward -= distance * 0.002

        if collision_count:
            reward -= collision_count * 6.0

        return float(reward)

    def _goal_distances(self) -> np.ndarray:
        """Distance from each robot to its assigned scenario goal."""
        return np.array(
            [
                np.linalg.norm(robot.position - self.targets[index])
                for index, robot in enumerate(self.robots)
            ],
            dtype=float,
        )

    def has_reached_goal(self, robot_index: int) -> bool:
        """Return whether a robot has reached its assigned scenario goal."""
        return self._arrival_awarded[robot_index]

    def get_sensor_readings(self, robot_index: int, max_range: Optional[float] = None) -> np.ndarray:
        """
        Return coarse 2D range readings for one robot.

        This is intentionally simple, but it establishes the shape needed for
        robotics-style perception experiments later.
        """
        robot = self.robots[robot_index]
        max_range = max_range or robot.sensor_range
        readings = np.full(self.sensor_ray_count, max_range, dtype=float)

        for ray_index in range(self.sensor_ray_count):
            angle = (ray_index / self.sensor_ray_count) * np.pi * 2.0
            direction = np.array([np.cos(angle), np.sin(angle)])
            distance = 0.0
            while distance < max_range:
                distance += 0.4
                probe_pos = robot.position + direction * distance
                if self._point_hits_world_or_obstacle(probe_pos):
                    readings[ray_index] = min(distance, max_range)
                    break

        return readings

    def _point_hits_world_or_obstacle(self, point: np.ndarray) -> bool:
        if np.any(point < 0.0) or np.any(point > self.world_size):
            return True

        probe = Robot(point, robot_id=-1)
        probe.size = 0.05
        return any(probe.collides_with(obstacle) for obstacle in self.obstacles)

    def render(self):
        """Render the environment."""
        if self.render_mode is None:
            return None

        if self.renderer is None and self.render_mode in {"human", "rgb_array"}:
            from ..core.renderer import Renderer

            self.renderer = Renderer(
                width=int(self.world_size[0] * 8),
                height=int(self.world_size[1] * 8),
                scale=8.0,
            )

        if not self.renderer:
            return None

        self.renderer.clear()
        self.renderer.draw_grid(cell_size=5.0)

        for zone in self.zones:
            self.renderer.draw_zone(zone)

        for obstacle in self.obstacles:
            self.renderer.draw_obstacle(obstacle)

        for index, target in enumerate(self.targets):
            name = self.target_names[index] if index < len(self.target_names) else f"Goal {index + 1}"
            self.renderer.draw_target(target, name=name)

        for index, robot in enumerate(self.robots):
            color = self.renderer.GREEN if self._arrival_awarded[index] else self.renderer.BLUE
            self.renderer.draw_robot(robot, color=color)
            readings = self.get_sensor_readings(index)
            self.renderer.draw_sensor_rays(robot, readings, robot.sensor_range)

        info = self._get_info()
        self.renderer.draw_status_panel(
            "Simulation",
            [
                ("Scenario", info["scenario"]),
                ("Step", f"{info['step']}/{self.max_steps}"),
                ("Arrived", f"{info['robots_arrived']}/{info['total_robots']}"),
                ("Collisions", str(info["collisions"])),
                ("Avg distance", f"{info['avg_goal_distance']:.2f}"),
            ],
            position=(10, 10),
        )

        self.renderer.update()
        self.renderer.tick(self.metadata["render_fps"])

        if self.render_mode == "rgb_array":
            return np.transpose(
                np.array(self.renderer.screen.convert()),
                axes=(1, 0, 2),
            )
        return None

    def close(self):
        """Clean up resources."""
        if self.renderer:
            self.renderer.close()
            self.renderer = None

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
                    speed=6.0,
                    bounds=tuple(self.world_size)
                )
                obstacle.center = center
                obstacle.radius = 8.0 + i * 2
                self.dynamic_obstacles.append(obstacle)
