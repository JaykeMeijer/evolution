import pygame
from time import time

from simulation.ui.ui import UI
from world.state import State
from world.world import XSIZE, YSIZE


FRAME_LIMIT = 1/1000

class Render:
    last_frame: float = 0

    def __init__(self, state: State, ui: UI):
        pygame.init()
        pygame.font.init()
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
            self.ui.draw(time() - self.last_frame, time_for_step)

            pygame.display.flip()
            self.last_frame = time()

    def _draw_world(self):
        self.screen.fill((255, 255, 255))

    def _draw_beasts(self):
        for beast in self.state.beasts:
            beast.draw(self.screen)
