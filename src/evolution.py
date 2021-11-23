from time import time
from typing import List
from threading import Thread

from beast.beast import Beast
from world.state import State
from world.render import Render
from world.world import distance

NUM_BEASTS = 50
MAX_REPLICATION_DISTANCE = 25
SIMULATION_STEP_TIME = 0.01

state = State()
render = Render(state)

time_for_step: float = 0.1

def setup_world():
    print("Setting up world")
    state.beasts += [Beast() for x in range(NUM_BEASTS)]


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


def game_loop():
    global time_for_step
    last_simulation_iteration = 0

    while state.active:
        if time() - last_simulation_iteration > SIMULATION_STEP_TIME:
            simulate_beasts()

            if len(state.beasts) == 0:
                state.active = False

            time_for_step = time() - last_simulation_iteration
            last_simulation_iteration = time()


def render_loop():
    while state.active:
        render.draw(time_for_step)


def run_simulation():
    print("Running simulation")
    simulation_thread = Thread(target=game_loop)
    simulation_thread.start()

    render_loop()
    print("Waiting for simulation thread to finish")
    simulation_thread.join()
    print("Shutting down")


if __name__ == "__main__":
    setup_world()
    run_simulation()
