from time import time, sleep
from typing import List

from beast.beast import Beast
from world.state import State
from world.render import Render
from world.world import distance

NUM_BEASTS = 50

state = State()
render = Render(state)

last_simulation_iteration = 0
simulation_step_time = 0.1

last_render_iteration = 0
render_step_time = 1/30

def setup_world():
    print("Setting up world")
    state.beasts += [Beast() for x in range(NUM_BEASTS)]


def simulate_beasts():
    new_beasts: List[Beast] = []
    dead_beasts: List[Beast] = []
    for beast in state.beasts:
        beast.step()

        if not beast.validate():
            dead_beasts.append(beast)

    for beast in dead_beasts:
        state.beasts.remove(beast)

    # TODO: Optimize
    for i, a in enumerate(state.beasts):
        for b in state.beasts[i+1:]:
            if distance(a.position, b.position) < 25:
                new_beasts += a.reproduce(b)

    state.beasts += new_beasts


def game_loop() -> bool:
    global simulation_step_time
    if time() - last_simulation_iteration > simulation_step_time:
        simulate_beasts()

        if len(state.beasts) == 0:
            return False

        simulation_step_time = time()

    return True


def run_simulation():
    while True:
        if not game_loop():
            break

        if not render.draw():
            break

        sleep(0.1)


if __name__ == "__main__":
    setup_world()
    run_simulation()
