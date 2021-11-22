class Action:
    pass


class Input:
    pass


class Move(Action):
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
