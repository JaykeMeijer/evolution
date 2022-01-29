import math
from typing import Tuple


def get_direction(from_point: Tuple[int, int], to_point: Tuple[int, int]) -> int:
    return round(math.degrees(
        math.atan2((to_point[0] - from_point[0]), -(to_point[1] - from_point[1]))
    ))


def translate(start: Tuple[int, int], direction: int, distance: int) -> Tuple[int, int]:
    radians = math.radians(direction)
    return (
        round(start[0] + math.sin(radians) * distance),
        round(start[1] - math.cos(radians) * distance)
    )
