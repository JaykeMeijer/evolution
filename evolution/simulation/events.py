import pygame

from evolution.simulation.ui.ui import UI
from evolution.world.state import State


class EventLoop:
    def __init__(self, state: State, ui: UI):
        self.state = state
        self.ui = ui

    def check_events(self):
        events = pygame.event.get()

        for event in events:
            self._handle_event(event)

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self.state.active = False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.ui.handle_mouse_click(pygame.mouse.get_pos())
