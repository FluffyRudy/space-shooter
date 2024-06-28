import pygame
from .container import Container
from src.utils.image_util import load_image
from config import UI_DIR


class GameoverUI:
    def __init__(self, pos: tuple[int, int]):
        self.container = Container(pos)

    def display(self, display_surface: pygame.Surface):
        self.container.display(display_surface)
