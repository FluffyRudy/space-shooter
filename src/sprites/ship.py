import pygame
from src.utils.image_util import load_frames
from src.timer.cooldown import Cooldown
from .state import Direction, State, Status
from .bullet import Bullet
from config import PLAYER_SHIP_DIR


class Ship(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], *groups):
        super().__init__(groups)

        self.frame_index = 0
        self.animation_speed = 0.25
        self.animations_list = load_frames(PLAYER_SHIP_DIR)
        self.direction = pygame.math.Vector2(0, 0)
        self.status = Status()

        self.image = self.animations_list[self.get_status()][0]
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = 4

        self.addition_groups = groups

        cooldown = 100
        self.cooldown_timer = Cooldown(cooldown)

    def animate(self):
        animation = self.animations_list[self.get_status()]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        frame_index = int(self.frame_index)
        self.image = animation[frame_index]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def update(self, *args, **kwargs):
        self.manage_status()
        self.animate()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def manage_status(self):
        if self.direction.x != 0:
            self.status.set_state(State.MOVEMENT)
        else:
            self.status.set_state(State.IDLE)

    def get_status(self):
        status = self.status.get_status()
        new_state = "idle"
        if status == State.MOVEMENT:
            if self.direction.x < 0:
                new_state = "left"
            else:
                new_state = "right"
        return new_state

    def create_bullet(self, num_bullets: int = 1):
        total_positions = num_bullets + ((num_bullets + 1) % 2)
        position_count = 0
        start_position = -(num_bullets // 2)

        while position_count < total_positions:
            bullet_position = self.rect.centerx, self.rect.top
            bullet = Bullet(
                bullet_position,
                (start_position, 0),
                start_position,
                [self.addition_groups],
            )
            start_position += 1
            position_count += 1
