from typing import Callable
import pygame
from collections import OrderedDict
from .container import Container
from .button import CustomButton
from src.utils.image_util import load_image
from src.settings import WIDTH, HEIGHT, G_SPRITE_SIZE
from config import UI_DIR


class MainMenuUI:
    def __init__(self, pos: tuple[int, int], event_action: dict):
        self.event_action = event_action
        self.container = Container(
            pos, "S P A C E  S H O O T E R", (WIDTH, HEIGHT), text_alpha_factor=(10, 0)
        )

        center_pos = (
            self.container.get_rect().width // 2,
            self.container.get_rect().height // 2,
        )
        positions = [
            (center_pos[0], center_pos[1] + i * G_SPRITE_SIZE * 2)
            for i in range(-1, 2, 1)
        ]
        start_button = CustomButton("start", positions[0])
        levels_button = CustomButton("levels", positions[1])
        exit_button = CustomButton("exit", positions[2])
        self.buttons = OrderedDict(
            start=start_button, levels=levels_button, _exit=exit_button
        )

    def display(self, display_surface: pygame.Surface):
        self.container.display(display_surface)
        for k in ["start", "levels", "_exit"]:
            self.buttons[k].display(self.container.get_surface())

    def update(self, event: pygame.event.Event):
        pass
