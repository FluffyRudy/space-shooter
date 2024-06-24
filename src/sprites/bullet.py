import pygame
from src.utils.image_util import load_frame
from config import BULLET_DIR


class Bullet(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int],
        offset_coor: tuple[int, int],
        sibling_offset_X: int = 0,
        *groups,
    ):
        super().__init__(groups)
        self.speed = 8
        self.direction = pygame.math.Vector2(0, -1)
        self.frames = load_frame(BULLET_DIR)
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.frames[0]
        position = (
            pos[0] + self.image.get_width() * offset_coor[0],
            pos[1] + self.image.get_height() * offset_coor[1],
        )
        self.rect = self.image.get_rect(center=position)

        self.sibling_offset_X = sibling_offset_X

    def animate(self):
        self.frame_index += self.animation_speed
        frame_index = int(self.frame_index) % len(self.frames)
        self.image = self.frames[frame_index]

    def update(self, *arg, **kwargs):
        self.animate()
        self.rect.x += self.speed * self.direction.x + self.sibling_offset_X
        self.rect.y += self.speed * self.direction.y
        if self.rect.bottom < 0:
            self.kill()
