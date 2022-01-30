from typing import Tuple

import pygame


def draw_multiline_text(screen: pygame.surface.Surface, text: str, location: Tuple[int, int], font: pygame.font.Font):
    lines = [font.render(line, True, (0, 0, 0)) for line in text.split("\n")]
    for i, line in enumerate(lines):
        screen.blit(line, (location[0], location[1] + font.get_linesize() * i))
