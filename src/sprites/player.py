import pygame
from .ship import Ship


class Player(Ship):
    def __init__(self, pos: tuple[int, int], *groups):
        super().__init__(pos, groups)

    def update(self):
        self.handle_movement()
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