from typing import List

from pygame.rect import Rect

from beast.beast import Beast
from datastructures.quadtree import QuadTree, QuadTreePoint
from world.state import state
from simulation.ui_constants import XSIZE, YSIZE

MAX_REPLICATION_DISTANCE = 15


def simulate_beasts():
    new_beasts: List[Beast] = []
    despawn_beasts: List[Beast] = []
    for beast in state.beasts:
        beast.step()
        beast.validate()
        if beast.despawnable():
            despawn_beasts.append(beast)

    for beast in despawn_beasts:
        state.beasts.remove(beast)

    tree = QuadTree(Rect(0, 0, XSIZE, YSIZE))
    for beast in state.beasts:
        tree.insert(QuadTreePoint(beast.position.x, beast.position.y, beast))

    for beast in state.beasts:
        nearby_beasts = tree.point_in_range(beast.position.tuple(), MAX_REPLICATION_DISTANCE)
        for nearby in nearby_beasts:
            if nearby.obj != beast:
                new_beasts += beast.reproduce(nearby.obj)

    state.beasts += new_beasts
