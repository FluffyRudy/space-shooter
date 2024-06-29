import pygame
from src.utils.image_util import load_image
from src.settings import WIDTH, HEIGHT
from config import UI_DIR


class Container:
    def __init__(self, pos: tuple[int, int]):
        path = UI_DIR / "menu" / "common" / "Window.png"
        self.image = load_image(path, None, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect(center=pos)
        print(self.precalculate_header_boxsize())

    def precalculate_header_boxsize(self):
        """i just used this way using a threshold to capture nearset family of color
        to detect position for header in image, this will do work done although its not so good way
        """

        x, y = self.image.get_width() // 2, 0
        midtop_color = self.image.get_at((x, y))[0]
        start_Y, end_y = (None, None)

        while abs(self.image.get_at((x, y))[0] - midtop_color) <= 10:
            y += 1
        start_y = y
        while abs(self.image.get_at((x, y))[0] - midtop_color) > 10:
            y += 1
        end_y = y

        return (start, end)

    def display(self, display_surface: pygame.Surface):
        display_surface.fill((138, 170, 169))
        display_surface.blit(self.image, self.rect.topleft)
