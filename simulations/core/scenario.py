"""Configurable scenario definitions for simulation environments."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Tuple, Union


SizeSpec = Union[float, Tuple[float, float]]


@dataclass(frozen=True)
class ObstacleSpec:
    """Blocking geometry in a scenario."""

    name: str
    position: Tuple[float, float]
    size: SizeSpec = 1.0
    kind: str = "obstacle"
    shape: str = "circle"


@dataclass(frozen=True)
class ZoneSpec:
    """Non-blocking semantic area in a scenario."""

    name: str
    position: Tuple[float, float]
    size: Tuple[float, float]
    kind: str = "zone"


@dataclass(frozen=True)
class RobotSpec:
    """Robot initial state and physical limits."""

    name: str
    position: Tuple[float, float]
    max_speed: float = 5.0
    acceleration: float = 10.0
    sensor_range: float = 8.0


@dataclass(frozen=True)
class TargetSpec:
    """Goal location for one robot."""

    name: str
    position: Tuple[float, float]
    kind: str = "goal"


@dataclass(frozen=True)
class ScenarioSpec:
    """A portable, user-editable simulation scenario."""

    name: str
    description: str
    world_size: Tuple[float, float]
    robots: Tuple[RobotSpec, ...] = field(default_factory=tuple)
    targets: Tuple[TargetSpec, ...] = field(default_factory=tuple)
    obstacles: Tuple[ObstacleSpec, ...] = field(default_factory=tuple)
    zones: Tuple[ZoneSpec, ...] = field(default_factory=tuple)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json(cls, path: Union[str, Path]) -> "ScenarioSpec":
        """Load a scenario from a JSON file."""
        with Path(path).open("r", encoding="utf-8") as scenario_file:
            payload = json.load(scenario_file)
        return cls.from_dict(payload)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ScenarioSpec":
        """Create a scenario from a plain dictionary."""
        world_size = _pair(payload.get("world_size", (100, 75)), "world_size")
        robots = tuple(_robot(item, index) for index, item in enumerate(payload.get("robots", ())))
        targets = tuple(_target(item, index) for index, item in enumerate(payload.get("targets", ())))
        obstacles = tuple(_obstacle(item, index) for index, item in enumerate(payload.get("obstacles", ())))
        zones = tuple(_zone(item, index) for index, item in enumerate(payload.get("zones", ())))

        return cls(
            name=str(payload.get("name", "Untitled Scenario")),
            description=str(payload.get("description", "")),
            world_size=world_size,
            robots=robots,
            targets=targets,
            obstacles=obstacles,
            zones=zones,
            metadata=dict(payload.get("metadata", {})),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serializable representation."""
        return {
            "name": self.name,
            "description": self.description,
            "world_size": list(self.world_size),
            "metadata": self.metadata,
            "robots": [
                {
                    "name": robot.name,
                    "position": list(robot.position),
                    "max_speed": robot.max_speed,
                    "acceleration": robot.acceleration,
                    "sensor_range": robot.sensor_range,
                }
                for robot in self.robots
            ],
            "targets": [
                {
                    "name": target.name,
                    "position": list(target.position),
                    "kind": target.kind,
                }
                for target in self.targets
            ],
            "obstacles": [
                {
                    "name": obstacle.name,
                    "position": list(obstacle.position),
                    "size": _size_to_json(obstacle.size),
                    "kind": obstacle.kind,
                    "shape": obstacle.shape,
                }
                for obstacle in self.obstacles
            ],
            "zones": [
                {
                    "name": zone.name,
                    "position": list(zone.position),
                    "size": list(zone.size),
                    "kind": zone.kind,
                }
                for zone in self.zones
            ],
        }


def _pair(value: Sequence[float], field_name: str) -> Tuple[float, float]:
    if len(value) != 2:
        raise ValueError(f"{field_name} must contain exactly two numbers")
    return float(value[0]), float(value[1])


def _size(value: Any) -> SizeSpec:
    if isinstance(value, (int, float)):
        return float(value)
    return _pair(value, "size")


def _size_to_json(value: SizeSpec) -> Union[float, list]:
    if isinstance(value, tuple):
        return list(value)
    return value


def _robot(payload: Mapping[str, Any], index: int) -> RobotSpec:
    return RobotSpec(
        name=str(payload.get("name", f"Robot {index + 1}")),
        position=_pair(payload.get("position", (5, 5)), "robot.position"),
        max_speed=float(payload.get("max_speed", 5.0)),
        acceleration=float(payload.get("acceleration", 10.0)),
        sensor_range=float(payload.get("sensor_range", 8.0)),
    )


def _target(payload: Mapping[str, Any], index: int) -> TargetSpec:
    return TargetSpec(
        name=str(payload.get("name", f"Target {index + 1}")),
        position=_pair(payload.get("position", (10, 10)), "target.position"),
        kind=str(payload.get("kind", "goal")),
    )


def _obstacle(payload: Mapping[str, Any], index: int) -> ObstacleSpec:
    size = _size(payload.get("size", 1.0))
    default_shape = "rect" if isinstance(size, tuple) else "circle"
    return ObstacleSpec(
        name=str(payload.get("name", f"Obstacle {index + 1}")),
        position=_pair(payload.get("position", (10, 10)), "obstacle.position"),
        size=size,
        kind=str(payload.get("kind", "obstacle")),
        shape=str(payload.get("shape", default_shape)),
    )


def _zone(payload: Mapping[str, Any], index: int) -> ZoneSpec:
    return ZoneSpec(
        name=str(payload.get("name", f"Zone {index + 1}")),
        position=_pair(payload.get("position", (10, 10)), "zone.position"),
        size=_pair(payload.get("size", (5, 5)), "zone.size"),
        kind=str(payload.get("kind", "zone")),
    )
