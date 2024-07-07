from typing import Callable, Optional
import pygame
from collections import OrderedDict
from .container import Container
from .button import CustomButton
from .scrollbox import Scrollbox
from src.storage.storage import Storage
from src.utils.image_util import load_image
from src.settings import WIDTH, HEIGHT, G_SPRITE_SIZE
from config import UI_DIR


class MainMenuUI:
    def __init__(self, pos: tuple[int, int], event_action: dict):
        self.event_action = event_action
        self.container = Container(
            pos, "S P A C E  S H O O T E R", (WIDTH, HEIGHT), text_alpha_factor=(10, 0)
        )
        self.container.get_surface().fill((0, 0, 0))

        center_pos = (
            self.container.get_rect().width // 2,
            self.container.get_rect().height // 2,
        )
        positions = [
            (center_pos[0], center_pos[1] + i * G_SPRITE_SIZE * 2)
            for i in range(-1, 3, 1)
        ]
        self.level_box = Scrollbox(
            (WIDTH // 2, self.container.header_box_height // 4 + HEIGHT // 2),
            lambda: self.level_box.toggle_visibility(),
        )
        self.shop_box = Scrollbox(
            (WIDTH // 2, self.container.header_box_height // 4 + HEIGHT // 2),
            lambda: self.shop_box.toggle_visibility(),
        )
        self.level_box.set_cell_callback(event_action["load_level"])
        self.init_loaded_level_range = Storage.get_current_level()
        for num_level in range(self.init_loaded_level_range):
            self.level_box.add_cell(f"{num_level + 1}", prefix="level")

        start_button = CustomButton("start", positions[0], event_action["play"])
        levels_button = CustomButton(
            "levels", positions[1], lambda: self.level_box.make_visible()
        )
        shop_button = CustomButton(
            "shop", positions[2], lambda: self.shop_box.make_visible()
        )
        exit_button = CustomButton("exit", positions[3], event_action["exit"])
        self.buttons = OrderedDict(
            start=start_button,
            levels=levels_button,
            shop=shop_button,
            _exit=exit_button,
        )

        self.display_level = False
        self.pressed_button = None

    def display(self, display_surface: pygame.Surface):
        self.container.display(display_surface)
        for button in self.buttons.values():
            button.display(self.container.get_surface())
        self.level_box.display(self.container.get_surface())
        self.shop_box.display(self.container.get_surface())
        self.container.display(display_surface)
        self.container.get_surface().fill((0, 0, 0))

    def update(self, event: Optional[pygame.event.Event]):
        is_event = event is not None
        if not is_event:
            return

        self.level_box.update(event)
        self.shop_box.update(event)

        if self.level_box.is_visible or event.type == pygame.MOUSEWHEEL:
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

    def update_levels(self, new_level: int):
        for level in range(self.init_loaded_level_range + 1, new_level + 1):
            self.level_box.add_cell(str(level), prefix="level")
