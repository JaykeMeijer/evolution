class Action:
    pass


class Input:
    pass


class MoveForward(Action):
    distance: int

    def __init__(self, distance: int):
        self.distance = distance


class Turn(Action):
    degrees: int

    def __init__(self, degrees: int):
        self.degrees = degrees
