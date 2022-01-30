from evolution.world.state import State


def toggle_pause(state: State):
    state.simulation_paused = not state.simulation_paused


def step(state: State):
    state.perform_step = True
