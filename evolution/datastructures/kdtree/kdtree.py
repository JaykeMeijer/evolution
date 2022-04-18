import math
from typing import Any, List, Optional, Tuple

import pygame
from pygame.rect import Rect

from evolution.util.math_helpers import square_dist

MAX_POINTS = 4


class KDTreePoint:
    def __init__(self, x: int, y: int, obj: Any):
        self.x = x
        self.y = y
        self.obj = obj

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
        if self.left is not None:
            count += self.left.num_points()
        if self.right is not None:
            count += self.right.num_points()
        if self.point is not None:
            count += 1
        return count

    def _insert(self, points: List[KDTreePoint]) -> None:
        if len(points) == 1:
            # Last point, make this a leave node
            self.point = points[0]
            return

        if self.vertical:
            key = lambda x: x.x
        else:
            key = lambda x: x.y

        sorted_points = sorted(points, key=key)
        median = math.floor(len(sorted_points) / 2)
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
            return Rect(self.area.left, self.area.top, self.area.width, (point.y - self.area.top))

    def _right_rect(self, point: KDTreePoint) -> Rect:
        if self.vertical:
            return Rect(point.x, self.area.top, (self.area.right - point.x), self.area.height)
        else:
            return Rect(self.area.left, point.y, self.area.width, (self.area.bottom - point.y))

    def find_nearest_neighbour(
        self,
        location: Tuple[int, int],
        obj: Any,
        current_best: float = math.inf,
        best_node: Optional[KDTreePoint] = None,
    ) -> Tuple[Optional[KDTreePoint], float]:
        node, squared_distance = self._find_nearest_neighbour(location, obj, current_best, best_node)
        return node, math.sqrt(squared_distance)

    def _find_nearest_neighbour(
        self,
        location: Tuple[int, int],
        obj: Any,
        current_best: float = math.inf,
        best_node: Optional[KDTreePoint] = None,
    ) -> Tuple[Optional[KDTreePoint], float]:
        if obj != self.point.obj:
            next_tree, other_tree = self._determine_next_subtree(location)
            local_dist = square_dist((self.point.x, self.point.y), location)
            return self._handle_tree(location, obj, next_tree, other_tree, local_dist, current_best, best_node)
        else:
            # If the node we are looking at is the object for which we are searching, we need to make sure to check both
            # trees
            best_node_1, current_best_1 = self._handle_tree(
                location, obj, self.left, self.right, 0, current_best, best_node
            )
            best_node_2, current_best_2 = self._handle_tree(
                location, obj, self.right, self.left, 0, current_best, best_node
            )
            if current_best_1 < current_best_2:
                return best_node_1, current_best_1
            else:
                return best_node_2, current_best_2

    def _handle_tree(
        self,
        location: Tuple[int, int],
        obj: Any,
        next_tree: Optional["KDTree"],
        other_tree: Optional["KDTree"],
        local_dist: float,
        current_best: float,
        best_node: Optional[KDTreePoint],
    ) -> Tuple[Optional[KDTreePoint], float]:
        if next_tree is None:
            return self._handle_leave(obj, local_dist, current_best, best_node)
        else:
            return self._handle_non_leave(location, obj, next_tree, other_tree, local_dist, current_best, best_node)

    def _determine_next_subtree(self, location: Tuple[int, int]) -> Tuple[Optional["KDTree"], Optional["KDTree"]]:
        if self.vertical:
            if location[0] < self.point.x:
                return self.left, self.right
            else:
                return self.right, self.left
        else:
            if location[1] < self.point.y:
                return self.left, self.right
            else:
                return self.right, self.left

    def _handle_leave(
        self,
        obj: Any,
        local_dist: float,
        current_best: float,
        best_node: Optional[KDTreePoint],
    ) -> Tuple[Optional[KDTreePoint], float]:
        if local_dist < current_best and self.point.obj != obj:
            return self.point, local_dist
        else:
            return best_node, current_best

    def _handle_non_leave(
        self,
        location: Tuple[int, int],
        obj: Any,
        next_tree: "KDTree",
        other_tree: Optional["KDTree"],
        local_dist: float,
        current_best: float,
        best_node: Optional[KDTreePoint],
    ) -> Tuple[Optional[KDTreePoint], float]:
        best_node, current_best = next_tree._find_nearest_neighbour(location, obj, current_best, best_node)
        if local_dist < current_best and self.point.obj != obj:
            current_best = local_dist
            best_node = self.point

        distance_to_plane = abs(location[0] - self.point.x) if self.vertical else abs(location[1] - self.point.y)
        if distance_to_plane**2 < current_best and other_tree is not None:
            return other_tree._find_nearest_neighbour(location, obj, current_best, best_node)
        else:
            return best_node, current_best

    def __str__(self) -> str:
        return self._print()

    def _print(self, tab=0) -> str:
        out_lines = []
        tab_str = " " * tab * 2
        out_lines.append(f"{tab_str}+ Subtree point - {self._printable_rect(self.area)} - {self.point}")

        if self.left is not None:
            out_lines.append(f"{tab_str}  L:\n{self.left._print(tab + 1)}")
        if self.right is not None:
            out_lines.append(f"{tab_str}  R:\n{self.right._print(tab + 1)}")

        return "\n".join(out_lines)

    @staticmethod
    def _printable_rect(rect):
        return f"X-range: {rect[0]}-{rect[0] + rect[2]}, Y-range: {rect[1]}-{rect[1] + rect[3]}"

    def draw(self, screen: pygame.surface.Surface):
        if self.vertical:
            begin = (self.point.x, self.area.top)
            end = (self.point.x, self.area.bottom)
            color = "green"
        else:
            begin = (self.area.left, self.point.y)
            end = (self.area.right, self.point.y)
            color = "orange"

        pygame.draw.aaline(screen, color, begin, end)
        if self.left:
            self.left.draw(screen)
        if self.right:
            self.right.draw(screen)
