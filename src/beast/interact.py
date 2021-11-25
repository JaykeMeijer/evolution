from dataclasses import dataclass
from typing import Optional


class Action:
    pass


@dataclass
class InputSet:
    distance_to_nearest_mate: Optional[float]
    direction_of_nearest_mate: Optional[float]


class MoveForward(Action):
    distance: int

    def __init__(self, distance: int):
        self.distance = distance


class Turn(Action):
    degrees: int

    def __init__(self, degrees: int):
        self.degrees = degrees
