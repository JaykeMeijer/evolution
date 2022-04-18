from typing import List, Tuple


class KDTreePoint:
    """
    A class representing a point contained in a KD Tree.

    :param x: X coordinate of the point
    :param y: Y coordinate of the point
    :param object_id: (Unique) integer identifying the object
    """
    def __init__(self, x: int, y: int, object_id: int) -> None: ...

    def string(self) -> str:
        """
        Returns a string representation of the point.
        """


class KDTree:
    """
    A KD Tree implemented in Rust.

    :param area: Tuple of int describing the area covered by the tree.
    :param points: List of KDTreePoint objects to insert into the tree.
    """
    def __init__(self, area: Tuple[int, int, int, int], points: List[KDTreePoint]) -> None: ...

    def string(self) -> str:
        """
        Returns a string representation of the tree.
        """

    def find_nearest_neighbour(self, location: Tuple[int, int], obj: int) -> Tuple[int, float]:
        """
        Find the nearest neighbour for an object at a given location.
        
        :param location: Tuple of int describing the location for which to search.
        :param obj: integer ID of current object, to prevent finding current object as nearest.
        :return: Tuple containing the ID of the nearest object and the distance it is away from here.
        """
