import math
from typing import Any, List, Optional, Tuple

from pygame.rect import Rect


class QuadTreePoint:
    def __init__(self, x: int, y: int, obj: Any):
        self.x = x
        self.y = y
        self.obj = obj

    def coord(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y}) - {self.obj}"


class Tree:
    def __init__(self, area: Rect, depth: int = 0, parent: "QuadTree" = None):
        self.area = area
        self.points: List[QuadTreePoint] = []
        self.depth = depth
        self.parent = parent

    def split(self) -> Tuple["QuadTree", "QuadTree", "QuadTree", "QuadTree"]:
        width = math.ceil(self.area.w / 2)
        height = math.ceil(self.area.h / 2)
        return (
            self._subtree(Rect(self.area.x, self.area.y, width, height)),
            self._subtree(Rect(self.area.x + width, self.area.y, width, height)),
            self._subtree(Rect(self.area.x, self.area.y + width, width, height)),
            self._subtree(Rect(self.area.x + width, self.area.y + height, width, height)),
        )

    def num_points(self):
        subtree_count = sum([subtree.num_points() for subtree in self.subtrees]) if self.subtrees is not None else 0
        return subtree_count + len(self.points)

    def _subtree(self, rect: Rect) -> "QuadTree":
        return QuadTree(rect, self.depth + 1, parent=self)

    def insert(self, point: QuadTreePoint) -> None:
        if self.subtrees is None and (len(self.points) < MAX_POINTS or self.depth > 10):
            self.points.append(point)
        else:
            if self.subtrees is None:
                if self.depth > 10:
                    raise RecursionError
                self.subtrees = self.split()
                for old_point in self.points:
                    self._insert_in_subtrees(old_point)
                self.points = []

            self._insert_in_subtrees(point)

    def _insert_in_subtrees(self, point):
        for subtree in self.subtrees:
            if subtree.in_tree(point):
                subtree.insert(point)

    def in_tree(self, point: QuadTreePoint) -> bool:
        return self.area.collidepoint(point.coord())

    def points_in_range(self, location: Tuple[int, int], range: int) -> List[QuadTreePoint]:
        found_points: List[QuadTreePoint] = []
        boundary = Rect(location[0] - range, location[1] - range, 2 * range, 2 * range)

        if not self.area.colliderect(boundary):
            return []

        if self.subtrees is not None:
            for tree in self.subtrees:
                found_points += tree.points_in_range(location, range)
        else:
            found_points += self._select_points_in_circle(location, range, boundary)
        return found_points

    def _select_points_in_circle(self, location: Tuple[int, int], range: int, boundary: Rect) -> List[QuadTreePoint]:
        return [
            point
            for point in self.points
            if boundary.collidepoint(point.coord()) and math.dist(location, point.coord()) <= range
        ]

    def __str__(self):
        return self.print()

    def print(self, tab=0):
        out_lines = []
        tab_str = " " * tab * 2
        out_lines.append(f"{tab_str}+ Subtree point - {self._printable_rect(self.area)}")
        for p in self.points:
            out_lines.append(f"{tab_str}  - {p}")

        if self.subtrees is not None:
            for s in self.subtrees:
                out_lines.append(s.print(tab + 1))

        return "\n".join(out_lines)

    @staticmethod
    def _printable_rect(rect):
        return f"X-range: {rect[0]}-{rect[0] + rect[2]}, Y-range: {rect[1]}-{rect[1] + rect[3]}"
