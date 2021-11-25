import math
from typing import Any, List, Optional, Tuple

from pygame.rect import Rect


MAX_POINTS = 4


class QuadTreePoint:
    def __init__(self, x: int, y: int, obj: Any):
        self.x = x
        self.y = y
        self.obj = obj

    def coord(self) -> Tuple[int, int]:
        return (self.x, self.y)


class QuadTree:
    subtrees: Optional[Tuple["QuadTree", "QuadTree", "QuadTree", "QuadTree"]] = None

    def __init__(self, area: Rect, depth: int = 0):
        self.area = area
        self.points: List[QuadTreePoint] = []
        self.depth = depth

    def split(self) -> Tuple["QuadTree", "QuadTree", "QuadTree", "QuadTree"]:
        width = math.ceil(self.area.w / 2)
        height = math.ceil(self.area.h / 2)
        return (
            self.subtree(Rect(self.area.x, self.area.y, width, height)),
            self.subtree(Rect(self.area.x + width, self.area.y, width, height)),
            self.subtree(Rect(self.area.x, self.area.y + width, width, height)),
            self.subtree(Rect(self.area.x + width, self.area.y + height, width, height)),
        )

    def subtree(self, rect: Rect) -> "QuadTree":
        return QuadTree(rect, self.depth + 1)

    def insert(self, point: QuadTreePoint) -> None:
        if len(self.points) < MAX_POINTS:
            self.points.append(point)
        else:
            if self.subtrees is None:
                self.subtrees = self.split()

            for subtree in self.subtrees:
                if subtree.in_tree(point):
                    subtree.insert(point)

    def in_tree(self, point: QuadTreePoint) -> bool:
        return self.area.collidepoint(point.coord())

    def point_in_range(self, location: Tuple[int, int], range: int) -> List[QuadTreePoint]:
        found_points: List[QuadTreePoint] = []
        boundary = Rect(location[0], location[1], 2 * range, 2 * range)

        if not self.area.colliderect(boundary):
            return []

        found_points += self._select_points_in_circle(location, range, boundary)

        if self.subtrees is not None:
            for tree in self.subtrees:
                found_points += tree.point_in_range(location, range)
        return found_points

    def _select_points_in_circle(self, location: Tuple[int, int], range: int, boundary: Rect) -> List[QuadTreePoint]:
        return [
            point
            for point in self.points
            if boundary.collidepoint(point.coord()) and math.dist(location, point.coord()) <= range
        ]
