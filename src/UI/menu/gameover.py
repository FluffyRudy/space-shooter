from typing import Callable
import pygame
from .container import Container
from .button import StateButton
from src.utils.image_util import load_image
from src.settings import WIDTH, HEIGHT, G_SPRITE_SIZE
from config import UI_DIR


class GameoverUI:
    def __init__(self, pos: tuple[int, int], event_action: dict):
        self.event_action = event_action
        self.container = Container(
            pos, "GAME_OVER", (WIDTH // 2, HEIGHT), text_alpha_factor=(10, 0)
        )

        center_pos = (
            self.container.get_rect().width // 2,
            self.container.get_rect().height // 2,
        )
        positions = [
            (center_pos[0] + i * G_SPRITE_SIZE, center_pos[1]) for i in range(-1, 2, 1)
        ]
        close_button = StateButton("close", positions[1], event_action["close"])
        replay_button = StateButton("replay", positions[0], event_action["replay"])
        main_menu = StateButton("main_menu", positions[2], event_action["main_menu"])
        self.buttons = {
            "close": close_button,
            "replay": replay_button,
            "main_menu": main_menu,
        }

    def display(self, display_surface: pygame.Surface):
        self.container.display(display_surface)
        for button in self.buttons.values():
            button.display(self.container.get_surface())

    def update(self, event: pygame.event.Event):
        is_event = event is not None
        if not is_event:
            return

        if event.type == pygame.MOUSEBUTTONUP:
            for button in self.buttons.values():
                converted_pos = self.container.convert_position(event.pos)
                if button.is_pressed(converted_pos):
                    button.trigger_action()
