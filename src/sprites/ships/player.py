from typing import Union, Literal
import pygame, math, random
from .ship import Ship
from .state import State
from ..weapons.bullet import Bullet
from ..weapons.projectile import create_projectile
from src.utils.image_util import load_frame
from src.timer.cooldown import Cooldown
from src.storage.storage import Storage
from src.soundmanager.soundmanager import Soundmanager
from src.settings import G_SPRITE_SIZE
from src.constants import BULLET_DAMAGE, BULLET_SPEED, ShipTypes, SHIELD
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
        self.coins = self.props.get("coins")

        self.limit_bound = pygame.display.get_surface().get_size()

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
            create_projectile(
                groups=[self.visible_group, self.bullet_group],
                relative_rect=self.rect,
                num_bullets=self.num_bullets,
                speed=Storage.get_player_data()[BULLET_SPEED],
                direction=(0, -1),
                damage=self.props[BULLET_DAMAGE],
                class_type=Bullet,
            )
            self.bullet_cooldown_timer.reset_time()

    def add_coins(self, coin_amount):
        self.coins += coin_amount
        self.props["coins"] = self.coins

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

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.limit_bound[0]:
            self.rect.right = self.limit_bound[0]
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.limit_bound[1]:
            self.rect.bottom = self.limit_bound[1]

    def get_damage_count(self):
        return max(0, self.props.get("health_count"))

    def increase_health_count(self, amount: int = 1):
        self.props["health_count"] += 1

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

    def make_immune(self):
        self.is_immune = True

    def make_vulnerable(self):
        self.is_immune = False
