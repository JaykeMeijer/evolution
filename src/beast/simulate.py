from typing import List

from beast.beast import Beast
from world.state import state
from world.world import distance

MAX_REPLICATION_DISTANCE = 25


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

    # TODO: Optimize
    for i, a in enumerate(state.beasts):
        for b in state.beasts[i+1:]:
            if distance(a.position, b.position) < MAX_REPLICATION_DISTANCE:
                new_beasts += a.reproduce(b)

    state.beasts += new_beasts