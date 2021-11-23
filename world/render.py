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

    def draw(self) -> bool:
        if time() - self.last_frame > FRAME_LIMIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            self._draw_world()
            self._draw_beasts()
            self._draw_stats()
            self._draw_framerate(time() - self.last_frame)

            pygame.display.flip()
            self.last_frame = time()

        return True

    def _draw_world(self):
        self.screen.fill((255, 255, 255))

    def _draw_beasts(self):
        for beast in self.state.beasts:
            beast.draw(self.screen)

    def _draw_stats(self):
        textsurface = self.font.render(f"Number of beasts: {len(self.state.beasts)}", True, (0, 0, 0))
        self.screen.blit(textsurface, (20, 20))

    def _draw_framerate(self, time_for_frame: float):
        textsurface = self.font.render(f"{round(1 / time_for_frame)} FPS", True, (0, 0, 0))
        self.screen.blit(textsurface, (900, 20))
