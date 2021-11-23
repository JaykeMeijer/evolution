from time import time

from world.state import State
from world.world import XSIZE, YSIZE

import pygame

FRAME_LIMIT = 1/1000

class Render:
    last_frame: float = 0

    def __init__(self, state: "State"):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("Calibri", 24)
        self.font.bold = True
        self.screen = pygame.display.set_mode([XSIZE, YSIZE])
        self.state = state

    def draw(self, time_for_step: float):
        if time() - self.last_frame > FRAME_LIMIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state.active = False

            self._draw_world()
            self._draw_beasts()
            self._draw_stats()
            self._draw_framerate(time() - self.last_frame, time_for_step)

            pygame.display.flip()
            self.last_frame = time()

    def _draw_world(self):
        self.screen.fill((255, 255, 255))

    def _draw_beasts(self):
        for beast in self.state.beasts:
            beast.draw(self.screen)

    def _draw_stats(self):
        stats = self.font.render(f"Number of beasts: {len(self.state.beasts)}", True, (0, 0, 0))
        self.screen.blit(stats, (20, 20))

    def _draw_framerate(self, time_for_frame: float, time_for_step: float):
        fps_text = self.font.render(f"{round(1 / time_for_frame)} FPS", True, (0, 0, 0))
        sps_text = self.font.render(f"{round(1 / time_for_step)} SPS", True, (0, 0, 0))
        self.screen.blit(fps_text, (900, 20))
        self.screen.blit(sps_text, (900, 60))
