from typing import Optional, Union, Literal
import pygame, enum
from src.utils.color_utils import random_rgba
from src.utils.math_util import calculate_center
from src.settings import WIDTH
from config import FONT_DIR


class ColorTransition:
    def __init__(
        self,
        text: str,
        size: int,
        font: Optional[pygame.font.Font] = None,
        factor: int = 0,
    ):
        self.font = pygame.font.Font(FONT_DIR / "Barcade-R4LM.otf", size)
        self.text = text
        if isinstance(font, pygame.font.Font):
            self.font = font
        self.initial_alpha = 20 if factor != 0 else 255
        self.max_alpha = 255
        self.alpha = self.initial_alpha
        self.transit_value = self.alpha
        self.factor = factor
        self.color = (255, 255, 255)

    def transit_alpha(self):
        if (
            self.transit_value < self.initial_alpha
            or self.transit_value > self.max_alpha
        ):
            self.factor *= -1
            if self.transit_value < 100:
                self.color = random_rgba()

        self.transit_value += self.factor
        self.alpha = int(self.transit_value)

    def transit_color(self, color: Union[pygame.Color, tuple[int, int, int]]):
        self.color = color

    def update_text(self, text: str):
        self.text = text

    def display(self, position: tuple[int, int], display_surface: pygame.Surface):
        text_surf = self.font.render(self.text, True, self.color)
        position = calculate_center((position[0], position[1]), text_surf.get_size())
        text_surf.set_alpha(self.alpha)
        self.transit_alpha()
        display_surface.blit(text_surf, position)
