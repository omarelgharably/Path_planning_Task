from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Cone:
    """A detected track cone.

    color: 0 indicates yellow (right side), 1 indicates blue (left side).
    Coordinates are expressed in a global/world frame, in meters.
    """

    x: float
    y: float
    color: int


@dataclass(frozen=True)
class CarPose:
    """Pose of the car in the global/world frame."""

    x: float
    y: float
    yaw: float


Path2D = List[Tuple[float, float]]
