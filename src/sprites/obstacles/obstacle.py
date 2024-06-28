import pygame
from pygame.math import Vector2
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
        self.hitbox = self.rect.inflate(-20, -25)

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
        self.hitbox = self.image.get_rect(center=self.rect.center)
        self.rect.center = self.hitbox.center

    def update(self, *arg, **kwargs):
        if self.has_collided:
            self.animate()
        self.hitbox.x += self.speed * self.direction.x
        self.hitbox.y += self.speed * self.direction.y
        self.rect.center = self.hitbox.center

    def active(self):
        self.has_collided = True

    def is_active(self):
        return self.has_collided
