import math
from typing import Dict, List, Tuple, cast

import matplotlib as mpl
import pygame

from beast.beast import Beast
from beast.brain.brain import BrainRenderer
from simulation.render_helpers import draw_multiline_text
from simulation.ui_constants import XSIZE, YSIZE
from simulation.ui.interactions import toggle_pause
from simulation.ui.ui_elements import Button, Element, Popup, ToggleButton
from world.state import State

mpl.use('Agg')

IMAGE_BASE_PATH = "../assets/images/ui"


class UI:
    screen: pygame.surface.Surface

    def __init__(self, state: State):
        self.state = state

        self.buttons: List[Button] = [
            ToggleButton(
                (10, YSIZE - 50),
                (40, 40),
                "pause",
                lambda: toggle_pause(self.state),
                f"{IMAGE_BASE_PATH}/play.png",
                f"{IMAGE_BASE_PATH}/pause.png",
            )
        ]

        self.static_elements: Dict[str, Element] = {
            "beast_stats": Popup(
                (XSIZE - 320, 20), (300, YSIZE - 40), "beast_stats"
            )
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
                return

        # Clicked on nothing
        self._unselect_all()

    def _display_beast_stats(self, beast: Beast):
        popup: Popup = cast(Popup, self.static_elements["beast_stats"])
        popup.set_text_dynamic(beast.stats_string)
        popup.set_image(self.brain_renderer.draw_brain(beast.brain))
        popup.shown = True

    def _unselect_all(self):
        popup: Popup = cast(Popup, self.static_elements["beast_stats"])
        popup.shown = False
