from time import time, sleep
from threading import Thread, current_thread

import matplotlib as mpl
import pygame

from evolution.beast.beast import Beast
from evolution.beast.simulate import simulate_beasts
from evolution.simulation.events import EventLoop
from evolution.world.state import state
from evolution.simulation.events import EventLoop
from evolution.simulation.render import Render
from evolution.simulation.ui.ui import UI

NUM_BEASTS = 50
SIMULATION_STEP_TIME = 0.01

pygame.init()
pygame.font.init()
mpl.use('Agg')

ui = UI(state)
render = Render(state, ui)
eventLoop = EventLoop(state, ui)

time_for_step: float = 0.1

def setup_world():
    print("Setting up world")
    state.beasts += [Beast() for _ in range(NUM_BEASTS)]


def _game_loop():
    global time_for_step
    last_simulation_iteration = 0

    while state.active:
        if not state.simulation_paused or state.perform_step:
            if time() - last_simulation_iteration > SIMULATION_STEP_TIME:
                simulate_beasts()

                if len(state.beasts) == 0:
                    state.active = False

                time_for_step = time() - last_simulation_iteration
                last_simulation_iteration = time()

            state.perform_step = False
        else:
            sleep(0.1)


def _render_loop():
    print("Starting render loop")
    while state.active:
        render.draw(time_for_step)


def _event_loop():
    print("Starting event loop")
    while state.active:
        eventLoop.check_events()


def run_simulation():
    print("Running simulation")
    simulation_thread = Thread(target=_game_loop, name="simulation")
    render_thread = Thread(target=_render_loop, name="render")
    current_thread().setName("event")
    simulation_thread.start()
    render_thread.start()

    _event_loop()
    print("Waiting for simulation and render threads to finish")
    simulation_thread.join()
    render_thread.join()
    print("Shutting down")


if __name__ == "__main__":
    setup_world()
    run_simulation()
