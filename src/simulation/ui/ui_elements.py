from dataclasses import dataclass
from typing import Optional, Tuple, Callable

import pygame

from beast.brain.brain import Brain
from simulation.render_helpers import draw_multiline_text


class Element:
    def __init__(self, location: Tuple[int, int], size: Tuple[int, int], name: str):
        self.name = name
        self.location = location
        self.size = size

        self.rect = pygame.rect.Rect(location[0], location[1], size[0], size[1])
        self.border_rect = pygame.rect.Rect(
            self.rect[0] - 1,
            self.rect[1] - 1,
            self.rect[2] + 2,
            self.rect[3] + 2,
        )

class Button(Element):
    def __init__(self, location: Tuple[int, int], size: Tuple[int, int], name: str, action: Callable):
        super().__init__(location, size, name)
        self.action = action

    def draw(self, screen: pygame.surface.Surface):
        pygame.draw.rect(screen, (0, 0, 0), self.rect, width=2, border_radius=5)

    def on_click(self):
        self.action()


class ToggleButton(Button):
    def __init__(
        self,
        location: Tuple[int, int],
        size: Tuple[int, int],
        name: str,
        action: Callable,
        image_active: str,
        image_inactive: str,
        active=False,
    ):
        self.active = active
        self.image_active = pygame.image.load(image_active)
        self.image_inactive = pygame.image.load(image_inactive)
        super().__init__(location, size, name, action)

    def draw(self, screen: pygame.surface.Surface):
        super().draw(screen)
        if self.active:
            screen.blit(self.image_active, self.location)
        else:
            screen.blit(self.image_inactive, self.location)

    def on_click(self):
        super().on_click()
        self.active = not self.active


class Popup(Element):
    def __init__(self, location: Tuple[int, int], size: Tuple[int, int], name: str):
        super().__init__(location, size, name)

        self.shown: bool = False
        self.text: str = ""
        self.text_dynamic: Optional[Callable] = None
        self.font: pygame.font = pygame.font.SysFont("Calibri", 18)
        self.image: Optional[pygame.surface.Surface] = None

    def set_text(self, text: str):
        self.text = text
        self.text_dynamic = None

    def set_text_dynamic(self, text_function: Callable):
        self.text_dynamic = text_function

    def set_image(self, image: pygame.surface.Surface):
        self.image = image

    def draw(self, screen: pygame.surface.Surface):
        if self.shown:
            pygame.draw.rect(screen, (0, 0, 0), self.border_rect, width=1, border_radius=5)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=5)
            if self.text_dynamic is not None:
                text = self.text_dynamic()
            else:
                text = self.text
            draw_multiline_text(screen, text, (self.location[0] + 10, self.location[1] + 10), self.font)

            if self.image is not None:
                screen.blit(self.image, (self.location[0], self.location[1] + 300))


@dataclass
class Image:
    size: Tuple[int, int]
    data: bytes
    format: str = "RGB"
