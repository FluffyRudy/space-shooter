import pygame
from .ship import Ship
from .bullet import Bullet


class Player(Ship):
    def __init__(self, pos: tuple[int, int], *groups):
        super().__init__(pos, groups)

    def update(self):
        self.handle_movement()
        self.cooldown_timer.handle_cooldown()
        super().update()

    def handle_movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_SPACE] and self.cooldown_timer.has_cooldown():
            self.create_bullet(num_bullets=3)
            self.cooldown_timer.reset_time()
