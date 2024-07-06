from typing import Union, Optional, Type
import pygame
from src.utils.image_util import load_frame
from src.settings import HEIGHT
from config import WEAPONS_DIR


class Projectile(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        pos: tuple[int, int],
        offset_coor: tuple[int, int],
        speed: float,
        direction: tuple[int, int],
        damage: int,
        frames_dir: str,
        sibling_offset_X: int = 0,
    ):
        super().__init__(groups)
        self.speed = speed
        self.damage = damage
        self.direction = pygame.math.Vector2(direction)
        self.frames = load_frame(WEAPONS_DIR / frames_dir)
        self.frame_index = 0
        self.animation_speed = 0.05

        self.image = self.frames[0]
        if self.direction.y > 0:
            self.image = pygame.transform.flip(self.image, False, True)
        position = (
            pos[0] + self.image.get_width() * offset_coor[0],
            pos[1] + self.image.get_height() * offset_coor[1],
        )
        self.rect = self.image.get_rect(center=position)
        self.sibling_offset_X = sibling_offset_X

    def set_direction(self, direction: tuple[int, int]):
        self.direction.x = direction[0]
        self.direction.y = direction[1]

    def get_damage(self):
        return self.damage

    def animate(self):
        self.frame_index += self.animation_speed
        frame_index = int(self.frame_index) % len(self.frames)
        self.image = self.frames[frame_index]

    def update(self, *args, **kwargs):
        self.rect.x += self.speed * self.direction.x + self.sibling_offset_X
        self.rect.y += self.speed * self.direction.y

        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

        self.animate()

    def handle_kill(self):
        self.kill()


def create_projectile(
    groups: list[pygame.sprite.Group],
    relative_rect: pygame.Rect,
    num_bullets,
    speed: float,
    damage: int,
    direction: tuple[int, int],
    class_type: Type,
):
    total_positions = num_bullets + ((num_bullets + 1) % 2)
    position_count = 0
    start_position = -(num_bullets // 2)

    y_position = relative_rect.top if direction[1] == -1 else relative_rect.bottom
    bullet_position = relative_rect.centerx, y_position
    while position_count < total_positions:
        bullet = class_type(
            groups=groups,
            pos=bullet_position,
            offset_coor=(start_position, 0),
            speed=speed,
            sibling_offset_X=start_position,
            direction=direction,
            damage=damage,
        )
        start_position += 1
        position_count += 1
