import pygame, math, random
from .ship import Ship
from .bullet import Bullet, create_bullet
from src.timer.cooldown import Cooldown
from src.storage.storage import Storage
from src.settings import DEFAULT_BULLET_SPEED, ShipTypes


class Player(Ship):
    def __init__(
        self,
        pos: tuple[int, int],
        visible_group: pygame.sprite.Group,
        bullet_group: pygame.sprite.Group,
    ):
        super().__init__(
            pos,
            ShipTypes.PLAYER,
            Storage.get_player_data(),
            visible_group,
            [],
            bullet_group,
        )
        self.auto_kill = False

        self.is_invincible = False
        self.invincility_cooldown_timer = Cooldown(
            self.props.get("invinciblity_cooldown_time")
        )

    def update(self, *args, **kwargs):
        self.handle_event()
        self.movement()
        self.bullet_cooldown_timer.handle_cooldown()
        self.invincility_cooldown_timer.handle_cooldown()
        self.handle_invincibility()
        super().update()

    def handle_event(self):
        if self.status.is_dead():
            return

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

        if keys[pygame.K_SPACE] and self.bullet_cooldown_timer.has_cooldown():
            create_bullet(
                groups=[self.visible_group, self.bullet_group],
                relative_rect=self.rect,
                num_bullets=1,
                speed=DEFAULT_BULLET_SPEED,
                direction=(0, -1),
                damage=self.props.get("damage"),
            )
            self.bullet_cooldown_timer.reset_time()

    def handle_invincibility(self):
        if (
            self.invincility_cooldown_timer.has_cooldown()
            and self.image.get_alpha() != 255
        ):
            self.image.set_alpha(255)
            self.is_invincible = False

        elif self.is_invincible and not self.status.is_dead():
            self.flicker_display()

    def flicker_display(self):
        self.image.set_alpha(math.sin(random.random()) * 255)

    def movement(self):
        self.rect.x += self.direction.x * self.props.get("speed")
        self.rect.y += self.direction.y * self.props.get("speed")

    def get_damage_count(self):
        return max(0, self.props.get("kill_damage_count"))
