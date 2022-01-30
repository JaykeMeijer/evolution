import math
from typing import Dict, List, Optional, Tuple, cast

import matplotlib as mpl
import pygame

from beast.beast import Beast
from beast.brain.brain import BrainRenderer
from simulation.render_helpers import draw_multiline_text
from simulation.ui_constants import XSIZE, YSIZE
from simulation.ui.interactions import toggle_pause, step
from simulation.ui.ui_elements import BeastPopup, Button, Element, Popup, PushButton, ToggleButton
from simulation.ui.ui_elements import TreePopup
from util.render_tree import render
from world.state import State, state

mpl.use('Agg')

IMAGE_BASE_PATH = "../assets/images/ui"


class UI:
    screen: pygame.surface.Surface

    def __init__(self, state: State):
        self.state = state
        self.selected_beast: Optional[Beast] = None

        self.buttons: List[Button] = [
            ToggleButton(
                (10, YSIZE - 50),
                (40, 40),
                "pause",
                lambda: toggle_pause(self.state),
                f"{IMAGE_BASE_PATH}/play.png",
                f"{IMAGE_BASE_PATH}/pause.png",
            ),
            PushButton(
                (60, YSIZE - 50),
                (40, 40),
                "step",
                lambda: step(self.state),
                f"{IMAGE_BASE_PATH}/step.png",
            ),
            PushButton(
                (110, YSIZE - 50),
                (40, 40),
                "tree",
                self._show_tree,
                f"{IMAGE_BASE_PATH}/step.png",
            ),
        ]

        self.static_elements: Dict[str, Element] = {
            "beast_stats": BeastPopup(),
            "tree": TreePopup(),
        }
        self.brain_renderer = BrainRenderer()

    def set_screen(self, screen: pygame.surface.Surface):
        self.screen = screen

    def set_font(self, font: pygame.font.Font):
        self.font = font

    def draw(self, time_for_frame: float, time_for_step: float):
        self._draw_stats()
        self._draw_framerate(time_for_frame, time_for_step)
        self._draw_buttons()
        self._draw_static_elements()

    def _draw_stats(self):
        stats = self.font.render(f"Number of beasts: {len(self.state.beasts)}", True, (0, 0, 0))
        self.screen.blit(stats, (10, 10))

    def _draw_framerate(self, time_for_frame: float, time_for_step: float):
        draw_multiline_text(
            self.screen,
            f"{round(1 / time_for_frame)} FPS\n{round(1 / time_for_step)} SPS",
            (YSIZE - 100, 10),
            self.font
        )

    def _draw_buttons(self):
        for button in self.buttons:
            if button.name == "step":
                if self.state.simulation_paused:
                    button.draw(self.screen)
            else:
                button.draw(self.screen)

    def _draw_static_elements(self):
        for element in self.static_elements.values():
            element.draw(self.screen)

    def handle_mouse_click(self, pos: Tuple[int, int]):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                button.on_click()
                return

        for beast in self.state.beasts:
            if math.dist(beast.position.tuple(), pos) <= beast.size:
                self._display_beast_stats(beast)
                self._unselect_beast()
                self.selected_beast = beast
                beast.selected = True
                return

        # Clicked on nothing
        self._unselect_all()

    def _display_beast_stats(self, beast: Beast):
        popup: Popup = cast(Popup, self.static_elements["beast_stats"])
        popup.set_text_dynamic(beast.stats_string)
        popup.set_image(self.brain_renderer.draw_brain(beast.brain))
        popup.shown = True

    def _unselect_all(self):
        for item in self.static_elements.values():
            if isinstance(item, Popup):
                item.shown = False

        self._unselect_beast()

    def _unselect_beast(self):
        if self.selected_beast is not None:
            self.selected_beast.selected = False
            self.selected_beast = None

    def _show_tree(self):
        tree_popup = cast(TreePopup, self.static_elements["tree"])
        tree_popup.set_image(render(self.state.tree))
        tree_popup.shown = True
