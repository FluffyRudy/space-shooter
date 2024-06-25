import pygame
from .ship import Ship
from .bullet import Bullet, create_bullet
from src.settings import DEFAULT_BULLET_SPEED, ShipTypes


class Player(Ship):
    def __init__(
        self,
        pos: tuple[int, int],
        visible_group: pygame.sprite.Group,
        bullet_group: pygame.sprite.Group,
    ):
        super().__init__(pos, ShipTypes.PLAYER, visible_group, [], bullet_group)

    def update(self, *args, **kwargs):
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
            create_bullet(
                groups=[self.visible_group, self.bullet_group],
                relative_rect=self.rect,
                num_bullets=5,
                speed=DEFAULT_BULLET_SPEED,
                direction=(0, -1),
            )
            self.cooldown_timer.reset_time()
