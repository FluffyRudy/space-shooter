import pygame
from pygame.math import Vector2
from src.soundmanager.soundmanager import Soundmanager
from src.utils.image_util import load_frame
from src.settings import ObstacleTypes
from config import OBSTACLES_DIR


class Obstacle(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int],
        obstacle_type: ObstacleTypes,
        visible_group: pygame.sprite.Group,
        base_group: pygame.sprite.Group,
    ):
        super().__init__([visible_group, base_group])
        asteroid_path = OBSTACLES_DIR / obstacle_type.name.lower()
        self.frames = load_frame(asteroid_path)
        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.has_collided = False
        self.direction = Vector2(0, 0)
        self.speed = 1

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1
            self.kill()
        frame_index = int(self.frame_index)
        self.image = self.frames[frame_index]
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, *arg, **kwargs):
        if self.has_collided:
            self.animate()
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y

    def active(self):
        if not self.has_collided:
            self.has_collided = True
            Soundmanager.play_sfx_sound("obstacle_destroy", channel=3)

    def is_active(self):
        return self.has_collided
