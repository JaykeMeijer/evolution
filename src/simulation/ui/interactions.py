from world.state import State


def toggle_pause(state: State):
    state.simulation_paused = not state.simulation_paused
