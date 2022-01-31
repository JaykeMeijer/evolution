import math
from typing import Tuple

import pygame

from evolution.util.math_helpers import get_direction, translate_non_rounded


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
    dash_length: int = 5,
):
    direction = get_direction(start, end)
    num_sections = math.floor(math.dist(start, end) / (dash_length * 2))
    current_point: Tuple[float, float] = start
    for _ in range(num_sections):
        temp_end = translate_non_rounded(current_point, direction, dash_length)
        pygame.draw.aaline(screen, color, _round_point(current_point), temp_end, width)
        current_point = translate_non_rounded(temp_end, direction, dash_length)


def _round_point(point: Tuple[float, float]) -> Tuple[int, int]:
    return (round(point[0]), round(point[1]))
