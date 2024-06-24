import pygame
from src.utils.image_util import load_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups):
        super.__init__(groups)

        self.image = 0
