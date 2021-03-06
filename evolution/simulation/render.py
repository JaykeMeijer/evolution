from time import time

import pygame

from evolution.simulation.ui.ui import UI
from evolution.world.state import State
from evolution.world.world import XSIZE, YSIZE

FRAME_LIMIT = 1 / 1000


class Render:
    last_frame: float = 0

    def __init__(self, state: State, ui: UI):
        self.font = pygame.font.SysFont("Calibri", 24)
        self.font.bold = True
        self.screen = pygame.display.set_mode([XSIZE, YSIZE])
        self.state = state
        self.ui = ui
        ui.set_screen(self.screen)
        ui.set_font(self.font)

    def draw(self, time_for_step: float):
        if time() - self.last_frame > FRAME_LIMIT:
            self._draw_world()
            self._draw_beasts()
            self._draw_kdtree()
            self.ui.draw(time() - self.last_frame, time_for_step)

            pygame.display.flip()
            self.last_frame = time()

    def _draw_world(self):
        self.screen.fill((255, 255, 255))

    def _draw_beasts(self):
        for beast in self.state.beasts:
            beast.draw(self.screen, self.state.render_nearest_mate, self.state.render_beast_name)

    def _draw_kdtree(self):
        if self.state.render_kdtree and self.state.tree is not None:
            self.state.tree.draw(self.screen)
