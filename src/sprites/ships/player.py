from typing import Union
import pygame, math, random
from .ship import Ship
from .state import State
from ..weapons.bullet import Bullet, create_bullet
from src.utils.image_util import load_frame
from src.timer.cooldown import Cooldown
from src.storage.storage import Storage
from src.soundmanager.soundmanager import Soundmanager
from src.settings import DEFAULT_BULLET_SPEED, ShipTypes, G_SPRITE_SIZE
from config import DEAD_EFFECT


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
        self.animations_list["dead"] = load_frame(
            DEAD_EFFECT, None, (G_SPRITE_SIZE, G_SPRITE_SIZE)
        )

        self.invincility_cooldown_timer = Cooldown(
            self.props.get("invincibility_cooldown_time")
        )
        self.auto_kill = False
        self.is_invincible = False
        self.is_immune = False

        self.num_bullets = 1

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
            Soundmanager.play_sfx_sound("shoot")
            create_bullet(
                groups=[self.visible_group, self.bullet_group],
                relative_rect=self.rect,
                num_bullets=self.num_bullets,
                speed=DEFAULT_BULLET_SPEED,
                direction=(0, -1),
                damage=self.props.get("bullet_damage"),
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
        return max(0, self.props.get("health_count"))

    def damage(self, damage: Union[int, None]):
        if self.is_invincible or self.is_immune:
            return
        if not self.auto_kill and not self.is_invincible:
            self.is_invincible = True
            self.invincility_cooldown_timer.reset_time()
        self.props["health_count"] -= 1
        if self.props["health_count"] <= 0:
            self.animation_speed = 0.1
            self.status.set_state(State.DEAD)
            self.direction *= 0

    def is_dead(self):
        return self.status.is_dead()
