import pygame
from .obstacle import Obstacle
from src.utils.image_util import load_frame
from src.settings import ObstacleTypes, HEIGHT, WIDTH
from config import OBSTACLES_DIR


class Asteroid(Obstacle):
    def __init__(
        self,
        pos: tuple[int, int],
        visible_group: pygame.sprite.Group,
        base_group: pygame.sprite.Group,
    ):
        pos = (pos[0] if (pos[0] < WIDTH) else (pos[0] - WIDTH - 1), pos[1])
        super().__init__(pos, ObstacleTypes.ASTEROID, visible_group, base_group)
        self.direction.y = 1 if pos[1] < HEIGHT // 2 else -1
