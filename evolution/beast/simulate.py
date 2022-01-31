from typing import List

from pygame.rect import Rect

from evolution.beast.beast import Beast
from evolution.datastructures.kdtree import KDTree, KDTreePoint
from evolution.simulation.ui_constants import XSIZE, YSIZE
from evolution.world.state import state

MAX_REPLICATION_DISTANCE = 15


def simulate_beasts():
    tree = _get_kd_tree()
    state.tree = tree
    _simulate_beasts(tree)
    state.beasts += _simulate_reproduction(tree)


def _get_kd_tree() -> KDTree:
    tree = KDTree(
        Rect(0, 0, XSIZE, YSIZE),
        insert_objects=[
            KDTreePoint(beast.position.x, beast.position.y, beast) for beast in state.beasts if beast.dead == 0
        ],
    )
    return tree


def _simulate_beasts(tree: KDTree):
    despawn_beasts: List[Beast] = []

    for beast in state.beasts:
        beast.step(tree)
        beast.validate()
        if beast.despawnable():
            despawn_beasts.append(beast)

    for beast in despawn_beasts:
        state.beasts.remove(beast)


def _simulate_reproduction(tree: KDTree) -> List[Beast]:
    new_beasts: List[Beast] = []
    for beast in state.beasts:
        nearest_beast, distance = tree.find_nearest_neighbour(beast.position.tuple(), beast)
        if nearest_beast is not None and distance < MAX_REPLICATION_DISTANCE:
            new_beasts += beast.reproduce(nearest_beast.obj)

            if len(new_beasts) == 0:
                # No reproduction, fight instead TODO improve
                beast.fight(nearest_beast.obj)

    return new_beasts
