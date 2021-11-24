import pygame
from typing import List, Tuple

from simulation.ui_constants import YSIZE
from simulation.ui.interactions import toggle_pause
from simulation.ui.ui_elements import Button, ToggleButton
from world.state import State


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

    def set_screen(self, screen: pygame.surface.Surface):
        self.screen = screen

    def set_font(self, font: pygame.font.Font):
        self.font = font

    def draw(self, time_for_frame: float, time_for_step: float):
        self._draw_stats()
        self._draw_framerate(time_for_frame, time_for_step)
        self._draw_buttons()

    def _draw_stats(self):
        stats = self.font.render(f"Number of beasts: {len(self.state.beasts)}", True, (0, 0, 0))
        self.screen.blit(stats, (10, 10))

    def _draw_framerate(self, time_for_frame: float, time_for_step: float):
        fps_text = self.font.render(f"{round(1 / time_for_frame)} FPS", True, (0, 0, 0))
        sps_text = self.font.render(f"{round(1 / time_for_step)} SPS", True, (0, 0, 0))
        self.screen.blit(fps_text, (800, 10))
        self.screen.blit(sps_text, (800, 50))

    def _draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)

    def handle_mouse_click(self, pos: Tuple[int, int]):
        for button in self.buttons:
            if button.rect.collidepoint(pos):
                button.on_click()
