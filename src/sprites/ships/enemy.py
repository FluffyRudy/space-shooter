import pygame, math, random
from .state import State
from .ship import Ship
from ..weapons.bullet import create_bullet
from src.storage.storage import Storage
from src.soundmanager.soundmanager import Soundmanager
from src.settings import DEFAULT_BULLET_SPEED, ShipTypes, HEIGHT, WIDTH, G_SPRITE_SIZE


class ShooterEnemy(Ship):
    def __init__(
        self,
        pos: tuple[int, int],
        visible_group: pygame.sprite.Group,
        base_group: pygame.sprite.Group,
        bullet_group: pygame.sprite.Group,
        offset_y: int = 0,
    ):
        super().__init__(
            pos,
            ShipTypes.SHOOTING_ENEMY,
            Storage.get_enemy_data("shooter"),
            visible_group,
            base_group,
            bullet_group,
        )
        self.offset_y = offset_y
        self.direction.x = random.choice([1, -1])
        self.prev_direction = self.direction.copy()

    def update(self, *args, **kwargs):
        relative_rect = kwargs.get("relative_rect")
        self.behave(relative_rect)
        self.movement()
        self.bullet_cooldown_timer.handle_cooldown()
        if self.bullet_cooldown_timer.has_cooldown():
            self.bullet_cooldown_timer.reset_time()
        super().update()

    def movement(self):
        velocity_x = self.direction.x * self.props.get("speed")
        velocity_y = self.direction.y * self.props.get("speed")
        self.rect.x += velocity_x
        self.rect.y += velocity_y + random.choice([-1, 1])

    def shoot(self):
        create_bullet(
            groups=[self.visible_group, self.bullet_group],
            relative_rect=self.rect,
            num_bullets=1,
            speed=DEFAULT_BULLET_SPEED,
            direction=(0, 1),
            damage=self.props.get("damage"),
        )

    def behave(self, relative_rect: pygame.Rect):
        if self.rect.left < 0:
            self.direction.x = 1
            self.prev_direction.x = 1
        elif self.rect.right > WIDTH:
            self.direction.x = -1
            self.prev_direction.x = -1
        if self.rect.top < self.offset_y:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if self.bullet_cooldown_timer.has_cooldown():
            x_dist = relative_rect.centerx - self.rect.centerx
            is_self_upper = self.rect.y < relative_rect.y + G_SPRITE_SIZE // 2
            if abs(x_dist) <= G_SPRITE_SIZE // 2 and is_self_upper:
                if self.direction.x != 0:
                    self.prev_direction.x = self.direction.x
                self.direction.x = 0
                self.shoot()
            else:
                self.direction.x = self.prev_direction.x


class SelfKillerEnemy(Ship):
    def __init__(
        self,
        pos: tuple[int, int],
        visible_group: pygame.sprite.Group,
        base_group: pygame.sprite.Group,
    ):
        super().__init__(
            pos,
            ShipTypes.SELF_KILL_ENEMY,
            Storage.get_enemy_data("self_killer"),
            visible_group,
            base_group,
            [],
        )
        self.animation_speed = 1
        self.direction.y = 1

        self.is_active = False

    def update(self, *args, **kwargs):
        relative_rect = kwargs.get("relative_rect")
        self.animate()
        self.rect.y += self.direction.y * self.props.get("speed") * 2
        if self.rect.bottom >= HEIGHT or self.rect.colliderect(relative_rect):
            self.status.set_state(State.DEAD)
            self.direction *= 0
            self.animation_speed = 0.1
        if (
            self.status.get_state() == State.DEAD
            and self.frame_index >= len(self.get_current_animation()) - 1
        ):
            self.kill()
        elif self.status.get_state() == State.DEAD and not self.is_active:
            self.is_active = True
            Soundmanager.play_sfx_sound("obstacle_destroy", channel=3)

    def calculate_vector(self, relative_rect: pygame.Rect):
        x_dist = self.rect.centerx - relative_rect.centerx
        y_dist = self.rect.centery - relative_rect.centery
        distance = math.hypot(x_dist, y_dist)
        if distance == 0:
            direction = (0, 0)
        else:
            direction = (x_dist / distance, y_dist / distance)

        return (distance, direction)
