import pygame
from src.utils.image_util import load_image
from src.settings import WIDTH, HEIGHT
from config import UI_DIR


class Container:
    def __init__(self, pos: tuple[int, int]):
        path = UI_DIR / "menu" / "common" / "Window.png"
        self.image = load_image(path, None, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect(center=pos)

    def display(self, display_surface: pygame.Surface):
        display_surface.fill("grey")
        display_surface.blit(self.image, self.rect.topleft)
