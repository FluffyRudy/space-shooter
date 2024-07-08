from typing import Union
import pygame
from src.UI.menu.button import CustomButton, StateButton
from src.animation.Text.colortransition import ColorTransition
from src.utils.color_utils import random_rgba
from src.utils.math_util import calculate_center
from src.utils.image_util import load_image
from src.settings import WIDTH, HEIGHT
from config import UI_DIR, FONT_DIR


class Container:
    def __init__(
        self,
        pos: tuple[int, int],
        header: str = "",
        size: tuple[int, int] = (WIDTH, HEIGHT),
        text_alpha_factor: tuple[int, int] = [0, 0],
    ):
        path = UI_DIR / "menu" / "common" / "Window.png"
        self.image = load_image(path, None, size)
        self.rect = self.image.get_rect(center=pos)
        self.original_image = self.image.copy()
        self.original_size = pygame.math.Vector2(self.rect.size)
        if len(header) > 0:
            self.header_box_height = self.calculate_header_boxheight()[1]
        else:
            self.header_box_height = 0

        self.header_text = ColorTransition(
            header,
            int(self.header_box_height // 1.5),
            factor=text_alpha_factor[0],
        )

    def get_rect(self):
        return self.rect

    def update_surface(self, surface: pygame.Surface):
        self.image = surface

    def get_surface(self):
        return self.image

    def calculate_header_boxheight(self):
        """i just used this way using a threshold to capture nearset family of color
        to detect position for header in image, this will do work done although its not a good way
        """
        x, y = self.image.get_width() // 2, 0
        midtop_color = self.image.get_at((x, y))[0]
        start_y, end_y = (None, None)

        while abs(self.image.get_at((x, y))[0] - midtop_color) <= 10:
            y += 1
        start_y = y
        while abs(self.image.get_at((x, y))[0] - midtop_color) > 10:
            y += 1
        end_y = y

        return (start_y, end_y)

    def add_header(self):
        self.header_text.display(
            (self.rect.width // 2, self.header_box_height // 2), self.image
        )

    def convert_position(self, pos: tuple[int, int]):
        pos_x = pos[0] - self.rect.left
        pos_y = pos[1] - self.rect.top
        return pos_x, pos_y

    def display(self, display_surface: pygame.Surface):
        self.add_header()
        display_surface.blit(self.image, self.rect.topleft)
        self.image.fill((0, 0, 0))
        self.image = self.original_image.copy()

    def update_font(self, font: pygame.font.Font):
        self.header_text.font = font

    def check_collision(self, pos: tuple[int, int]):
        return self.rect.collidepoint(self.convert_position(pos))
