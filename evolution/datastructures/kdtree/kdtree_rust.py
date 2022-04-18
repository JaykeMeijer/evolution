import math
from typing import Any, Dict, List, Optional, Tuple

import pygame
import rust_kdtree
from pygame.rect import Rect


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
        insert_objects: List[KDTreePoint] = [],
    ):
        self.rust_points: List[rust_kdtree.KDTreePoint] = []
        self.lookup: Dict[int, KDTreePoint] = {}
        for obj in insert_objects:
            self.rust_points.append(rust_kdtree.KDTreePoint(obj.x, obj.y, obj.obj.id))
            self.lookup[obj.obj.id] = obj
        self.tree = rust_kdtree.KDTree((area.left, area.top, area.width, area.height), self.rust_points)

    def num_points(self):
        return len(self.rust_points)

    def find_nearest_neighbour(
        self,
        location: Tuple[int, int],
        obj: Any,
    ) -> Tuple[Optional[KDTreePoint], float]:
        node_id, distance = self.tree.find_nearest_neighbour(location, obj.id)
        return self.lookup.get(node_id), distance

    def __str__(self) -> str:
        return self.tree.string()

    def draw(self, screen: pygame.surface.Surface):
        raise NotImplementedError
