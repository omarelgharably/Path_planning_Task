from __future__ import annotations

import math
from typing import List, Optional, Tuple

from src.models import CarPose, Cone, Path2D

Point = Tuple[float, float]
Waypoint = Tuple[Point, Point]

YELLOW = 0
BLUE = 1

DEFAULT_TRACK_WIDTH = 3.0
STEP = 0.25
MIN_LENGTH = 6.0
MAX_LENGTH = 10.0
MIN_WAYPOINT_GAP = 0.5


class PathPlanning:
    def __init__(self, car_pose: CarPose, cones: List[Cone]):
        self.car_pose = car_pose
        self.cones = cones

    def generatePath(self) -> Path2D:
        car = (self.car_pose.x, self.car_pose.y)
        heading = (math.cos(self.car_pose.yaw), math.sin(self.car_pose.yaw))
        blue = self._cones_by_distance(BLUE)
        yellow = self._cones_by_distance(YELLOW)

        waypoints: Optional[List[Waypoint]] = None
        if len(blue) >= 3 > len(yellow):
            waypoints = arc_waypoints(blue[:3], yellow, is_left=True)
        elif len(yellow) >= 3 > len(blue):
            waypoints = arc_waypoints(yellow[:3], blue, is_left=False)
        if waypoints is None:
            waypoints = pair_waypoints(blue, yellow, heading)

        waypoints = follow_neighbours(drop_close_waypoints([(car, heading)] + waypoints))
        curve = hermite_spline(waypoints)
        curve = extend_straight(curve, waypoints[-1][1], MIN_LENGTH)
        return resample(curve, STEP, MAX_LENGTH)

    def _cones_by_distance(self, color: int) -> List[Point]:
        car = (self.car_pose.x, self.car_pose.y)
        points = [(cone.x, cone.y) for cone in self.cones if cone.color == color]
        return sorted(points, key=lambda p: math.dist(car, p))


def pair_waypoints(blue: List[Point], yellow: List[Point], heading: Point) -> List[Waypoint]:
    width = track_width(blue, yellow)
    waypoints = []
    for i in range(max(len(blue), len(yellow))):
        if i < len(blue) and i < len(yellow):
            left, right = blue[i], yellow[i]
        elif i < len(blue):
            left = blue[i]
            right = add(left, scale(right_of(side_direction(blue, heading)), width))
        else:
            right = yellow[i]
            left = add(right, scale(left_of(side_direction(yellow, heading)), width))
        waypoints.append((midpoint(left, right), right_of(unit(sub(left, right)))))
    return waypoints


def arc_waypoints(cones: List[Point], others: List[Point], is_left: bool) -> Optional[List[Waypoint]]:
    circle = circle_through(*cones)
    if circle is None:
        return None
    centre, radius = circle

    first, last = cones[0], cones[-1]
    turn = 1 if cross(sub(first, centre), sub(last, centre)) > 0 else -1

    if others:
        width = sum(abs(math.dist(o, centre) - radius) for o in others) / len(others)
    else:
        width = DEFAULT_TRACK_WIDTH
    boundary_is_inner = is_left == (turn > 0)
    mirrored_radius = radius + width if boundary_is_inner else radius - width
    centre_radius = (radius + mirrored_radius) / 2
    if centre_radius < MIN_WAYPOINT_GAP:
        return None

    start_angle = math.atan2(first[1] - centre[1], first[0] - centre[0])
    waypoints = []
    for i in range(int(MAX_LENGTH) + 1):
        angle = start_angle + turn * i / centre_radius
        point = (centre[0] + centre_radius * math.cos(angle), centre[1] + centre_radius * math.sin(angle))
        direction = (-turn * math.sin(angle), turn * math.cos(angle))
        waypoints.append((point, direction))
    return waypoints


def track_width(blue: List[Point], yellow: List[Point]) -> float:
    widths = [math.dist(b, y) for b, y in zip(blue, yellow)]
    return sum(widths) / len(widths) if widths else DEFAULT_TRACK_WIDTH


def side_direction(side: List[Point], heading: Point) -> Point:
    if len(side) < 2:
        return heading
    return unit(sub(side[-1], side[0]))


def circle_through(a: Point, b: Point, c: Point) -> Optional[Tuple[Point, float]]:
    d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    if abs(d) < 1e-6:
        return None
    a2, b2, c2 = a[0] ** 2 + a[1] ** 2, b[0] ** 2 + b[1] ** 2, c[0] ** 2 + c[1] ** 2
    ux = (a2 * (b[1] - c[1]) + b2 * (c[1] - a[1]) + c2 * (a[1] - b[1])) / d
    uy = (a2 * (c[0] - b[0]) + b2 * (a[0] - c[0]) + c2 * (b[0] - a[0])) / d
    return (ux, uy), math.dist((ux, uy), a)


def drop_close_waypoints(waypoints: List[Waypoint]) -> List[Waypoint]:
    result = [waypoints[0]]
    for waypoint in waypoints[1:]:
        if math.dist(waypoint[0], result[-1][0]) >= MIN_WAYPOINT_GAP:
            result.append(waypoint)
    return result


def follow_neighbours(waypoints: List[Waypoint]) -> List[Waypoint]:
    if len(waypoints) < 3:
        return waypoints
    points = [p for p, _ in waypoints]
    result = [waypoints[0]]
    for i in range(1, len(points) - 1):
        result.append((points[i], unit(sub(points[i + 1], points[i - 1]))))
    result.append((points[-1], unit(sub(points[-1], points[-2]))))
    return result


def hermite_spline(waypoints: List[Waypoint], samples_per_segment: int = 20) -> List[Point]:
    curve = []
    for (p0, d0), (p1, d1) in zip(waypoints, waypoints[1:]):
        length = math.dist(p0, p1)
        m0, m1 = scale(d0, length), scale(d1, length)
        for s in range(samples_per_segment):
            t = s / samples_per_segment
            h00 = 2 * t ** 3 - 3 * t ** 2 + 1
            h10 = t ** 3 - 2 * t ** 2 + t
            h01 = -2 * t ** 3 + 3 * t ** 2
            h11 = t ** 3 - t ** 2
            curve.append(tuple(h00 * p0[k] + h10 * m0[k] + h01 * p1[k] + h11 * m1[k] for k in (0, 1)))
    curve.append(waypoints[-1][0])
    return curve


def extend_straight(points: List[Point], direction: Point, min_length: float) -> List[Point]:
    points = list(points)
    while polyline_length(points) < min_length:
        points.append(add(points[-1], direction))
    return points


def resample(points: List[Point], step: float, max_length: float) -> List[Point]:
    result = [points[0]]
    travelled = 0.0
    next_at = step
    for a, b in zip(points, points[1:]):
        segment = math.dist(a, b)
        while segment > 0 and next_at <= travelled + segment and next_at <= max_length:
            t = (next_at - travelled) / segment
            result.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
            next_at += step
        travelled += segment
    return result


def polyline_length(points: List[Point]) -> float:
    return sum(math.dist(a, b) for a, b in zip(points, points[1:]))


def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1])


def sub(a: Point, b: Point) -> Point:
    return (a[0] - b[0], a[1] - b[1])


def scale(a: Point, k: float) -> Point:
    return (a[0] * k, a[1] * k)


def midpoint(a: Point, b: Point) -> Point:
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def cross(a: Point, b: Point) -> float:
    return a[0] * b[1] - a[1] * b[0]


def unit(a: Point) -> Point:
    norm = math.hypot(a[0], a[1]) or 1.0
    return (a[0] / norm, a[1] / norm)


def left_of(a: Point) -> Point:
    return (-a[1], a[0])


def right_of(a: Point) -> Point:
    return (a[1], -a[0])
