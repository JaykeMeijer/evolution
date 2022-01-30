import math
from typing import Tuple

import pygame

from evolution.util.math_helpers import get_direction, translate


def draw_multiline_text(screen: pygame.surface.Surface, text: str, location: Tuple[int, int], font: pygame.font.Font):
    lines = [font.render(line, True, (0, 0, 0)) for line in text.split("\n")]
    for i, line in enumerate(lines):
        screen.blit(line, (location[0], location[1] + font.get_linesize() * i))


def draw_dashed_line(
    screen: pygame.surface.Surface,
    color: pygame.color.Color | Tuple[int, int, int] | int,
    start: Tuple[int, int],
    end: Tuple[int, int],
    width: int,
    dash_length: int = 3,
):
    direction = get_direction(start, end)
    sections = math.floor(math.dist(start, end) / dash_length / 2)
    current_point = start
    for _ in range(sections):
        temp_end = translate(current_point, direction, dash_length)
        pygame.draw.line(screen, color, current_point, temp_end, width)
        current_point = translate(temp_end, direction, dash_length)
