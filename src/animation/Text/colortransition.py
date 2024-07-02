from typing import Optional, Union
import pygame
from src.utils.color_utils import random_rgba
from src.utils.math_util import calculate_center
from src.settings import WIDTH
from config import FONT_DIR


class ColorTransition:
    """
    A class to manage text rendering with smooth color and alpha transitions.

    Attributes:
        text (str): The text to render.
        size (int): The font size.
        font (Optional[pygame.font.Font]): The custom font to use (default: None).
        factor (int): The rate of alpha transition (default: 0).
        change_color (bool): Whether to change color dynamically (default: True).

    Methods:
        transit_alpha(): Update the alpha value for smooth transition.
        transit_color(color: Union[pygame.Color, tuple[int, int, int]]): Update the text color.
        update_text(text: str): Update the text content.
        display(position: tuple[int, int], display_surface: pygame.Surface):
            Render and display the text on a surface at a given position.

    Usage:
        Initialize the ColorTransition object with text and optional parameters,
        then call display() in your main loop to render and update the text.

    Note:
        If a custom font is provided, the `size` attribute will be overridden by the
        custom font's size.

    """

    def __init__(
        self,
        text: str,
        size: int,
        font: Optional[pygame.font.Font] = None,
        factor: int = 0,
        change_color: bool = True,
    ):
        """
        Initialize ColorTransition with text, font size, and optional parameters.

        Args:
            text (str): The text to render.
            size (int): The font size.
            font (Optional[pygame.font.Font]): The custom font to use (default: None).
            factor (int): The rate of alpha transition (default: 0).
            change_color (bool): Whether to change color dynamically (default: True).
        """
        self.font = pygame.font.Font(FONT_DIR / "Barcade-R4LM.otf", size)
        self.text = text
        if isinstance(font, pygame.font.Font):
            self.font = font
        self.initial_alpha = 20 if factor != 0 else 255
        self.max_alpha = 255
        self.alpha = self.initial_alpha
        self.transit_value = self.alpha
        self.factor = factor
        self.change_color = change_color
        self.color = (255, 255, 255)

    def transit_alpha(self):
        """
        Update the alpha value for smooth transition.
        Reverse direction if it exceeds initial or maximum alpha.
        """
        if (
            self.transit_value < self.initial_alpha
            or self.transit_value > self.max_alpha
        ):
            self.factor *= -1
            if self.change_color and self.transit_value < 100:
                self.color = random_rgba()

        self.transit_value += self.factor
        self.alpha = int(self.transit_value)

    def transit_color(self, color: Union[pygame.Color, tuple[int, int, int]]):
        """
        Update the text color.

        Args:
            color (Union[pygame.Color, tuple[int, int, int]]): The color to set.
        """
        self.color = color

    def update_text(self, text: str):
        """
        Update the text content.

        Args:
            text (str): The new text content.
        """
        self.text = text

    def display(self, position: tuple[int, int], display_surface: pygame.Surface):
        """
        Render and display the text on a surface at a given position.

        Args:
            position (tuple[int, int]): The position to render the text.
            display_surface (pygame.Surface): The surface to render the text on.
        """
        text_surf = self.font.render(self.text, True, self.color)
        position = calculate_center((position[0], position[1]), text_surf.get_size())
        text_surf.set_alpha(self.alpha)
        self.transit_alpha()
        display_surface.blit(text_surf, position)
