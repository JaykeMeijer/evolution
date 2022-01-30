import math
from typing import Any, List, Optional, Tuple

from pygame.rect import Rect

MAX_POINTS = 4


class KDTreePoint:
    def __init__(self, x: int, y: int, obj: Any):
        self.x = x
        self.y = y
        self.obj = obj

    def coord(self) -> Tuple[int, int]:
        return (self.x, self.y)

    def __str__(self):
        return f"({self.x}, {self.y}) - {self.obj}"


class KDTree:
    def __init__(
        self,
        area: Rect,
        depth: int = 0,
        insert_objects: List[KDTreePoint] = [],
        parent: "KDTree" = None,
        vertical: bool = True,
    ):
        self.area = area
        self.left: Optional[KDTree] = None
        self.right: Optional[KDTree] = None
        self.depth = depth
        self.parent = parent
        self.vertical = vertical

        self._insert(insert_objects)

    def num_points(self):
        count = 0
        if self.left:
            count += self.left.num_points()
        if self.right:
            count += self.right.num_points()
        if self.point:
            count += 1
        return count

    def _insert(self, points: List[KDTreePoint]) -> None:
        if len(points) == 1:
            self.point = points[0]
            return

        # Find median
        if self.vertical:
            key = lambda x: x.x
        else:
            key = lambda x: x.y

        sorted_points = sorted(points, key=key)
        median = math.ceil(len(sorted_points) / 2)
        self.point = sorted_points[median]
        left_points = sorted_points[:median]
        right_points = sorted_points[median + 1 :]
        if len(left_points) > 0:
            self.left = KDTree(self._left_rect(self.point), self.depth + 1, left_points, self, not self.vertical)
        if len(right_points) > 0:
            self.right = KDTree(self._right_rect(self.point), self.depth + 1, right_points, self, not self.vertical)

    def _left_rect(self, point: KDTreePoint) -> Rect:
        if self.vertical:
            return Rect(self.area.left, self.area.top, (point.x - self.area.left), self.area.height)
        else:
            return Rect(self.area.left, self.area.top, self.area.width, point.y)

    def _right_rect(self, point: KDTreePoint) -> Rect:
        if self.vertical:
            return Rect(point.x, self.area.top, (self.area.right - point.x), self.area.height)
        else:
            return Rect(self.area.left, point.y, self.area.width, (self.area.height - point.y))

    def find_nearest_neighbour(
        self, location: Tuple[int, int], object: Any, current_best: float = math.inf
    ) -> Tuple[Optional[KDTreePoint], float]:
        if self.vertical:
            if location[0] < self.point.x:
                next_tree = self.left
                other_tree = self.right
            else:
                next_tree = self.right
                other_tree = self.left
        else:
            if location[1] < self.point.y:
                next_tree = self.left
                other_tree = self.right
            else:
                next_tree = self.right
                other_tree = self.left

        local_dist = math.dist(self.point.coord(), location)
        if next_tree is None:
            if self.point.obj != object and local_dist > current_best:
                current_best = local_dist
                return self.point, current_best
            else:
                return None, current_best
        else:
            best_node, best_dist = next_tree.find_nearest_neighbour(location, object, current_best)
            if self.point is not None and self.point.obj != object and local_dist < best_dist:
                best_dist = local_dist
                best_node = self.point

            if math.dist(location, self.point.coord()) < best_dist and other_tree is not None:
                return other_tree.find_nearest_neighbour(location, object, current_best)
            else:
                return best_node, best_dist

    def __str__(self):
        return self.print()

    def print(self, tab=0):
        out_lines = []
        tab_str = " " * tab * 2
        out_lines.append(f"{tab_str}+ Subtree point - {self._printable_rect(self.area)} - {self.point}")

        if self.left is not None:
            out_lines.append(f"{tab_str}  L:\n{self.left.print(tab + 1)}")
        if self.right is not None:
            out_lines.append(f"{tab_str}  R:\n{self.right.print(tab + 1)}")

        return "\n".join(out_lines)

    @staticmethod
    def _printable_rect(rect):
        return f"X-range: {rect[0]}-{rect[0] + rect[2]}, Y-range: {rect[1]}-{rect[1] + rect[3]}"
