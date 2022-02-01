import math
import random
from typing import Tuple


def get_direction(from_point: Tuple[int, int], to_point: Tuple[int, int]) -> int:
    """
    Get the direction from one point to another. Is given as degrees, with 0/360 being up, 90 right, 180 down etc.

    Note that this is in PyGame coordinates, with (0,0) being the top-left, meaning that the Y-direction is reversed
    compared to mathmetical coordinates.
    """
    return round(math.degrees(math.atan2((to_point[0] - from_point[0]), -(to_point[1] - from_point[1]))))


def translate(start: Tuple[int, int], direction: int, distance: int) -> Tuple[int, int]:
    """
    Determine coordinates at a certain distance and in a certain direction (in degrees) from the given coordinate.

    Note that this is in PyGame coordinates, with (0,0) being the top-left, meaning that the Y-direction is reversed
    compared to mathmetical coordinates.
    """
    radians = math.radians(direction)
    return (round(start[0] + math.sin(radians) * distance), round(start[1] - math.cos(radians) * distance))


def translate_non_rounded(start: Tuple[float, float], direction: int, distance: int) -> Tuple[float, float]:
    radians = math.radians(direction)
    return (start[0] + math.sin(radians) * distance, start[1] - math.cos(radians) * distance)


def square_dist(point_a: Tuple[int, int], point_b: Tuple[int, int]):
    return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2


def rand_int_lower_range(a: int, b: int, strength: int):
    result = math.inf
    for _ in range(strength):
        result = min(result, random.randint(a, b))
    return result
