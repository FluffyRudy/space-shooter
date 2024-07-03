from typing import Union
import pygame
from src.utils.image_util import load_frame
from src.settings import HEIGHT
from config import WEAPONS_DIR


class Laser(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        pos: tuple[int, int],
        damage: int,
    ):
        LASER_DIR = WEAPONS_DIR / "laser"
        super().__init__(groups)
        self.damage = damage
        self.frames = load_frame(LASER_DIR)
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.frames[0]

        self.rect = self.image.get_rect(
            midtop=(pos[0], pos[1] - self.image.get_height() * 0.99)
        )

    def get_damage(self):
        return self.damage

    def animate(self):
        self.frame_index += self.animation_speed
        frame_index = int(self.frame_index) % len(self.frames)
        self.image = self.frames[frame_index]
