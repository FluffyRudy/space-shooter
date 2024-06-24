import pygame
from src.utils.image_util import load_frame
from config import BULLET_DIR


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups):
        super().__init__(groups)
        self.speed = 5
        self.direction = pygame.math.Vector2(0, 1)
        self.frames = load_frame(BULLET_DIR)
        print(BULLET_DIR)
        print(self.frames)
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        frame_index = int(self.frame_index) % len(self.frames)
        self.image = self.frame_index[frame_index]

    def update(self, *arg, **kwargs):
        self.animate()
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y
        if self.rect.bottom < -self.rect.height:
            self.kill()
