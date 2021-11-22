from time import time

from world.state import State
from world.world import XSIZE, YSIZE

import pygame

FRAME_LIMIT = 1/30

class Render:
    last_frame: float = 0

    def __init__(self, state: "State"):
        pygame.init()
        self.screen = pygame.display.set_mode([XSIZE, YSIZE])
        self.state = state

    def draw(self) -> bool:
        if time() - self.last_frame > FRAME_LIMIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            self.screen.fill((255, 255, 255))

            for beast in self.state.beasts:
                beast.draw(self.screen)

            pygame.display.flip()

            self.last_frame = time()
            print(len(self.state.beasts))

        return True
