import pygame, math, random
from .state import State
from .ship import Ship
from .bullet import create_bullet
from src.storage.storage import get_enemy_data
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
            get_enemy_data().get("shooter"),
            visible_group,
            base_group,
            bullet_group,
        )
        self.offset_y = offset_y
        self.cooldown_timer.update_cooldown(500)
        self.direction.x = random.choice([1, -1])

    def update(self, *args, **kwargs):
        relative_rect = kwargs.get("relative_rect")
        self.update_direction_x(relative_rect)

        self.movement()
        self.cooldown_timer.handle_cooldown()
        if self.cooldown_timer.has_cooldown():
            self.cooldown_timer.reset_time()
        super().animate()

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
        )

    def update_direction_x(self, relative_rect: pygame.Rect):
        if self.rect.left < 0:
            self.direction.x = 1
        elif self.rect.right > WIDTH:
            self.direction.x = -1
        if self.rect.top < self.offset_y:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if self.cooldown_timer.has_cooldown():
            x_dist = relative_rect.centerx - self.rect.centerx
            if abs(x_dist) <= G_SPRITE_SIZE:
                self.shoot()


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
            get_enemy_data().get("self_killer"),
            visible_group,
            [],
            [],
        )
        self.animation_speed = 1
        self.direction.y = 1

    def update(self, *args, **kwargs):
        self.animate()
        self.rect.y += self.direction.y * self.props.get("speed") * 2
        if self.rect.bottom >= HEIGHT:
            self.status.set_state(State.DEAD)
            self.direction *= 0
            self.animation_speed = 0.1
        if (
            self.status.get_status() == State.DEAD
            and self.frame_index >= len(self.get_current_animation()) - 1
        ):
            self.kill()

    def calculate_vector(self, relative_rect: pygame.Rect):
        x_dist = self.rect.centerx - relative_rect.centerx
        y_dist = self.rect.centery - relative_rect.centery
        distance = math.hypot(x_dist, y_dist)
        if distance == 0:
            direction = (0, 0)
        else:
            direction = (x_dist / distance, y_dist / distance)

        return (distance, direction)