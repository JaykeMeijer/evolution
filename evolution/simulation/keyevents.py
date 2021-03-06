from evolution.simulation.ui.ui import UI
from evolution.world.state import State


def handle_key_press(key: int, state: State, ui: UI):
    if key in keymap:
        action, args = keymap[key]
        action(state, ui, *args)


def _toggle_state(state: State, ui: UI, property: str):
    if hasattr(state, property) and isinstance(getattr(state, property), bool):
        setattr(state, property, (not getattr(state, property)))


def _set_state_false(state: State, ui: UI, property: str):
    if hasattr(state, property) and isinstance(getattr(state, property), bool):
        setattr(state, property, False)


def _set_state_true(state: State, ui: UI, property: str):
    if hasattr(state, property) and isinstance(getattr(state, property), bool):
        setattr(state, property, True)


def _call_UI_function(state: State, ui: UI, function: str):
    if hasattr(ui, function) and callable(getattr(ui, function)):
        func = getattr(ui, function)
        func()


keymap = {
    27: (_call_UI_function, ["handle_escape"]),
    32: (_toggle_state, ["simulation_paused"]),
    109: (_toggle_state, ["render_nearest_mate"]),
    110: (_toggle_state, ["render_beast_name"]),
    115: (_set_state_true, ["perform_step"]),
    116: (_toggle_state, ["render_kdtree"]),
}
