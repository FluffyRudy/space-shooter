from typing import Literal, Callable
import pygame
from src.utils.image_util import load_image
from src.settings import G_SPRITE_SIZE
from config import UI_DIR, FONT_DIR

state_ = Literal["active", "normal"]
type_ = Literal[
    "forward", "backward", "close", "main_menu", "ok", "pause", "play", "replay"
]


class StateButton:
    base_dir = UI_DIR / "buttons"

    @classmethod
    def get_button(cls, state_: state_, type_: type_):
        return cls.base_dir / state_ / f"{type_}.png"

    def __init__(self, button_type: type_, pos: tuple[int, int], action: Callable):
        self.normal = load_image(
            StateButton.get_button("normal", button_type),
            None,
            (G_SPRITE_SIZE, G_SPRITE_SIZE),
        )
        self.active = load_image(
            StateButton.get_button("active", button_type),
            None,
            (G_SPRITE_SIZE, G_SPRITE_SIZE),
        )
        self.state_list = [self.normal, self.active]
        self.current = 0
        self.rect = self.normal.get_rect(center=pos)
        self.pos = pos
        self.action: Callable = action
        self.button_type = button_type

    def display(self, display_surface: pygame.Surface):
        display_surface.blit(self.state_list[self.current], self.rect.topleft)

    def toggle(self):
        self.current = (self.current + 1) % len(self.state_list)

    def trigger_action(self):
        self.action()

    def inactive(self):
        self.current = 0

    def is_pressed(self, pos: tuple[int, int]):
        return self.rect.collidepoint(pos)


class CustomButton:
    def __init__(self, image_path: str, text: str, pos: tuple[int, int]):
        self.image = load_image(image_path)
        self.rect = self.image.get_rect(topleft=pos)
        self.font = pygame.font.Font(
            FONT_DIR / "BarcadeNoBarBold-gzXq.otf", min(self.rect.size)
        )

    def display(self, display_surface: pygame.Surface):
        display_surface.blit(self.image, self.rect.topleft)
