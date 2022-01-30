from dataclasses import dataclass
from typing import Optional


class Action:
    pass


@dataclass
class InputSet:
    distance_to_nearest_mate: Optional[float]
    direction_of_nearest_mate: Optional[float]

    def all_none(self):
        return all([val is None for val in vars(self).values()])

    def __str__(self):
        distance = f"{self.distance_to_nearest_mate:.2f}" if self.distance_to_nearest_mate is not None else "-"
        direction = f"{self.direction_of_nearest_mate:}" if self.direction_of_nearest_mate is not None else "-"
        return "Inputs:\n" f"  distance_nearest_mate: {distance}\n" f"  direction_nearest_mate: {direction}"


class Noop(Action):
    pass


class MoveForward(Action):
    pass


class Turn(Action):
    degrees: int

    def __init__(self, degrees: int):
        self.degrees = degrees
