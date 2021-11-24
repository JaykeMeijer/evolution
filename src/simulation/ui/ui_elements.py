from typing import Tuple, Callable

import pygame
from pygame import image


class Button:
    def __init__(self, location: Tuple[int, int], size: Tuple[int, int], name: str, action: Callable):
        self.name = name
        self.location = location
        self.size = size
        self.action = action

        self.rect = pygame.rect.Rect(location[0], location[1], size[0], size[1])

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
