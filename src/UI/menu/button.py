from typing import Literal, Callable, Optional
import pygame
from src.utils.math_util import calculate_center
from src.utils.image_util import load_image
from src.settings import G_SPRITE_SIZE
from config import UI_DIR, FONT_DIR

state_ = Literal["active", "normal"]
type_ = Literal[
    "forward", "backward", "close", "main_menu", "ok", "pause", "play", "replay"
]


class Button:
    def __init__(self, pos: tuple[int, int], action: Callable):
        self.pos = pos
        self.action = action

    def is_pressed(self, pos: tuple[int, int]):
        return self.rect.collidepoint(pos)

    def trigger_action(self):
        self.action()


class StateButton(Button):
    base_dir = UI_DIR / "buttons"

    @classmethod
    def get_button(cls, state_: state_, type_: type_):
        return cls.base_dir / state_ / f"{type_}.png"

    def __init__(self, button_type: type_, pos: tuple[int, int], action: Callable):
        super().__init__(pos, action)
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
        self.button_type = button_type

    def display(self, display_surface: pygame.Surface):
        display_surface.blit(self.state_list[self.current], self.rect.topleft)

    def toggle(self):
        self.current = (self.current + 1) % len(self.state_list)

    def inactive(self):
        self.current = 0


class CustomButton(Button):
    def __init__(
        self,
        text: str,
        pos: tuple[int, int],
        action: Callable,
        size: Optional[tuple[int, int]] = None,
    ):
        super().__init__(pos, action)
        table_path = UI_DIR / "menu" / "common" / "Table.png"
        if size:
            self.image = load_image(table_path, None, size)
        else:
            self.image = load_image(table_path)
        self.rect = self.image.get_rect(center=pos)
        self.font = pygame.font.Font(
            FONT_DIR / "BarcadeNoBarBold-gzXq.otf", sum(self.rect.size) // 10
        )
        self.text = text
        self.text_surf = self.font.render(text, True, (255, 255, 255))

    def update_text(self, text: str):
        self.text_surf = self.font.render(text, True, (255, 255, 255))

    def display(self, display_surface: pygame.Surface):
        display_surface.blit(self.image, self.rect.topleft)
        self.image.blit(
            self.text_surf,
            calculate_center(self.image.get_size(), self.text_surf.get_size()),
        )
