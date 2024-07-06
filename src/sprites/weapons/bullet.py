from typing import Union, Optional, Callable
import pygame
from .projectile import Projectile
from src.utils.image_util import load_frame
from src.settings import HEIGHT
from config import WEAPONS_DIR


class Bullet(Projectile):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        pos: tuple[int, int],
        offset_coor: tuple[int, int],
        speed: float,
        direction: tuple[int, int],
        damage: int,
        sibling_offset_X: int = 0,
    ):
        BULLET_DIR = WEAPONS_DIR / "bullet"
        super().__init__(
            groups,
            pos,
            offset_coor,
            speed,
            direction,
            damage,
            BULLET_DIR,
            sibling_offset_X,
        )
