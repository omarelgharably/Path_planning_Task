from __future__ import annotations

from typing import Dict, List, Tuple

from src.models import CarPose, Cone


_SCENARIOS: Dict[str, Tuple[List[Cone], CarPose]] = {
    "1": (
        [],
        CarPose(x=0.0, y=0.0, yaw=0.0),
    ),

    "2": (
        [Cone(x=1.0, y=3.0, color=1), Cone(x=1.0, y=1.0, color=0)],
        CarPose(x=0.0, y=0.0, yaw=0.4),
    ),

    "3": (
        [
            Cone(x=1.0, y=3.0, color=1),
            Cone(x=3.0, y=3.0, color=1),
            Cone(x=1.0, y=1.0, color=0),
            Cone(x=3.0, y=1.0, color=0),
        ],
        CarPose(x=0.0, y=0.0, yaw=0.8),
    ),

    "4": (
        [Cone(x=4.0, y=2.0, color=0)],
        CarPose(x=0.0, y=0.0, yaw=1.2),
    ),

    "5": (
        [Cone(x=4.0, y=2.0, color=0), Cone(x=3.0, y=2.0, color=0)],
        CarPose(x=0.0, y=0.0, yaw=1.6),
    ),

    "6": (
        [
            Cone(x=4.0, y=4.0, color=1),
            Cone(x=4.0, y=2.0, color=0),
            Cone(x=3.0, y=2.0, color=0),
        ],
        CarPose(x=0.0, y=0.0, yaw=2.0),
    ),

    "7": (
        [
            Cone(x=2.0, y=3.0, color=1),
            Cone(x=4.0, y=3.0, color=1),
            Cone(x=2.0, y=2.0, color=0),
        ],
        CarPose(x=0.0, y=0.0, yaw=1.4),
    ),

    "8": (
        [Cone(x=3.0, y=3.0, color=1), Cone(x=5.0, y=3.0, color=1)],
        CarPose(x=0.0, y=0.0, yaw=1.8),
    ),

    "9": (
        [Cone(x=3.0, y=3.0, color=1)],
        CarPose(x=0.0, y=0.0, yaw=0.2),
    ),

    "10": (
        [Cone(x=5.0, y=3.0, color=1), Cone(x=5.0, y=2.0, color=0)],
        CarPose(x=0.0, y=0.0, yaw=0.6),
    ),

    "11": (
        [
            Cone(x=1.0, y=3.0, color=1),
            Cone(x=4.0, y=5.0, color=1),
            Cone(x=1.0, y=2.0, color=0),
            Cone(x=4.0, y=2.0, color=0),
        ],
        CarPose(x=0.0, y=0.0, yaw=1.0),
    ),

    "12": (
        [Cone(x=5.0, y=2.0, color=0)],
        CarPose(x=0.0, y=0.0, yaw=1.4),
    ),

    "13": (
        [Cone(x=5.0, y=3.0, color=0), Cone(x=5.0, y=1.0, color=0)],
        CarPose(x=0.0, y=0.0, yaw=0.1),
    ),

    "14": (
        [
            Cone(x=3.0, y=5.0, color=1),
            Cone(x=3.0, y=2.0, color=0),
            Cone(x=5.0, y=2.0, color=0),
        ],
        CarPose(x=0.0, y=0.0, yaw=5.2),
    ),

    "15": (
        [
            Cone(x=2.0, y=5.0, color=1),
            Cone(x=3.0, y=4.0, color=1),
            Cone(x=3.0, y=2.0, color=0),
        ],
        CarPose(x=0.0, y=0.0, yaw=1.6),
    ),

    "16": (
        [Cone(x=0.0, y=3.0, color=1), Cone(x=2.0, y=5.0, color=1)],
        CarPose(x=0.0, y=0.0, yaw=0.2),
    ),

    "17": (
        [Cone(x=3.0, y=5.0, color=1)],
        CarPose(x=0.0, y=0.0, yaw=0.6),
    ),

    "18": (
        [Cone(x=2.0, y=4.0, color=1), Cone(x=4.0, y=3.0, color=0)],
        CarPose(x=0.0, y=0.0, yaw=1.0),
    ),

    "19": (
        [
            Cone(x=2.0, y=3.0, color=1),
            Cone(x=5.0, y=3.0, color=1),
            Cone(x=2.0, y=0.0, color=0),
            Cone(x=5.0, y=2.0, color=0),
        ],
        CarPose(x=0.0, y=0.0, yaw=1.4),
    ),

    "20": (
        [Cone(x=0.0, y=2.0, color=0)],
        CarPose(x=0.0, y=0.0, yaw=1.8),
    ),

    "21": (
        [
            Cone(x=1.0, y=1.6, color=1),
            Cone(x=2.2, y=2.3, color=1),
            Cone(x=3.2, y=3.5, color=1),
        ],
        CarPose(x=0.0, y=0.0, yaw=0.0),
    ),

    "22": (
        [
            Cone(x=1.6, y=0.9, color=0),
            Cone(x=2.1, y=2.0, color=0),
            Cone(x=3.3, y=3.0, color=0),
        ],
        CarPose(x=0.0, y=0.0, yaw=1.57),
    ),

    "23": (
        [
            Cone(x=2.75, y=-0.76, color=0),
            Cone(x=4.2, y=0.46, color=0),
            Cone(x=5.2, y=2.1, color=0),
        ],
        CarPose(x=0.0, y=0.0, yaw=0.0),
    ),

    "24": (
        [
            Cone(x=1.0, y=1.5, color=1),
            Cone(x=2.5, y=1.5, color=1),
            Cone(x=4.0, y=1.5, color=1),
        ],
        CarPose(x=0.0, y=0.0, yaw=0.0),
    ),
}


def get_scenario_names() -> List[str]:
    return sorted(_SCENARIOS.keys(), key=lambda s: int(s))


def make_scenario(name: str) -> Tuple[List[Cone], CarPose]:
    if name not in _SCENARIOS:
        valid = ", ".join(get_scenario_names())
        raise ValueError(f"Unknown scenario '{name}'. Valid options: {valid}")
    cones, car = _SCENARIOS[name]
    return list(cones), CarPose(x=car.x, y=car.y, yaw=car.yaw)
