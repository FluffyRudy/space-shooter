from typing import Callable, Optional
import pygame
from collections import OrderedDict
from .container import Container
from .button import CustomButton
from .scrollbox import Scrollbox
from src.settings import WIDTH, HEIGHT, G_SPRITE_SIZE


class PauseMenu:
    def __init__(self, pos: tuple[int, int], event_action: dict):
        self.event_action = event_action
        self.container = Container(
            pos, "P A U S E  M E N U", (WIDTH, HEIGHT), text_alpha_factor=(10, 0)
        )
        self.container.get_surface().fill((0, 0, 0))

        center_pos = (
            self.container.get_rect().width // 2,
            self.container.get_rect().height // 2,
        )
        positions = [
            (center_pos[0], center_pos[1] + i * G_SPRITE_SIZE * 2)
            for i in range(-1, 2, 1)
        ]

        resume_button = CustomButton("resume", positions[0], event_action["resume"])
        restart_button = CustomButton("restart", positions[1], event_action["restart"])
        quit_button = CustomButton("quit", positions[2], event_action["quit"])

        self.buttons = OrderedDict(
            resume=resume_button,
            restart=restart_button,
            quit=quit_button,
        )

        self.pressed_button = None

    def display(self, display_surface: pygame.Surface):
        self.container.display(display_surface)
        for button in self.buttons.values():
            button.display(self.container.get_surface())

        self.container.display(display_surface)
        self.container.get_surface().fill((0, 0, 0))

    def update(self, event: Optional[pygame.event.Event]):
        is_event = event is not None
        if not is_event:
            return

        for button in self.buttons.values():
            converted_pos = self.container.convert_position(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and button.is_pressed(
                converted_pos
            ):
                self.pressed_button = button
                button.rect.inflate_ip(-10, -10)
            elif event.type == pygame.MOUSEBUTTONUP and button.is_pressed(
                converted_pos
            ):
                button.rect.inflate_ip(10, 10)
                button.trigger_action()
                self.pressed_button = None

        if self.pressed_button:
            mouse_pos = pygame.mouse.get_pos()
            if not self.pressed_button.is_pressed(mouse_pos):
                self.pressed_button.rect.inflate_ip(10, 10)
                self.pressed_button = None
