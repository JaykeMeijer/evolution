from typing import List

from pygame.rect import Rect

from evolution.beast.beast import Beast
from evolution.datastructures.quadtree import QuadTree, QuadTreePoint
from evolution.simulation.ui_constants import XSIZE, YSIZE
from evolution.world.state import state

MAX_REPLICATION_DISTANCE = 15


def simulate_beasts():
    tree = _get_quad_tree()
    state.tree = tree
    _simulate_beasts(tree)
    state.beasts += _simulate_reproduction(tree)


def _get_quad_tree() -> QuadTree:
    tree = QuadTree(Rect(0, 0, XSIZE, YSIZE))
    for beast in state.beasts:
        tree.insert(QuadTreePoint(beast.position.x, beast.position.y, beast))
    return tree


def _simulate_beasts(tree: QuadTree):
    despawn_beasts: List[Beast] = []

    for beast in state.beasts:
        beast.step(tree)
        beast.validate()
        if beast.despawnable():
            despawn_beasts.append(beast)

    for beast in despawn_beasts:
        state.beasts.remove(beast)


def _simulate_reproduction(tree: QuadTree) -> List[Beast]:
    new_beasts: List[Beast] = []

    for beast in state.beasts:
        nearby_beasts = tree.points_in_range(beast.position.tuple(), MAX_REPLICATION_DISTANCE)
        for nearby in nearby_beasts:
            if nearby.obj != beast:
                new_beasts += beast.reproduce(nearby.obj)

    return new_beasts
