import pytest
from beast.beast import Beast
from world.world import Position


@pytest.mark.parametrize(
    "beast_position, beast_rotation, other_position, expected",
    [
        (Position(0, 0), 0, Position(10, 0), 90),
        (Position(10, 0), 0, Position(0, 0), -90),
        (Position(0, 0), 0, Position(0, 10), 180),
        (Position(0, 10), 0, Position(0, 0), 0),
        (Position(0, 0), 90, Position(10, 0), 0),
        (Position(10, 0), -90, Position(0, 0), 0),
        (Position(0, 0), 180, Position(0, 10), 0),
        (Position(0, 10), 180, Position(0, 0), 180),
        (Position(1, 1), 0, Position(2, 2), 135),
        (Position(1, 1), 0, Position(0, 2), 225),
        (Position(1, 1), 145, Position(2, 2), -10),
        (Position(1, 1), 359, Position(2, 2), 136),
    ]
)
def test__get_relative_direction(beast_position, beast_rotation, other_position, expected):
    beast = Beast(None, beast_position)
    beast.rotation = beast_rotation
    other = Beast(None, other_position)
    _assert_equal_direction(beast._get_relative_direction(other), expected)


def _assert_equal_direction(one, two):
    assert (
        one == two
        or one % 360 == two
    )
