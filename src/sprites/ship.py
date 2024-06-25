import pygame, random, math
from src.utils.image_util import load_frames, load_frame
from src.timer.cooldown import Cooldown
from .state import Direction, State, Status
from .bullet import Bullet
from src.settings import DEFAULT_BULLET_SPEED, ShipTypes
from config import PLAYER_SHIP_DIR, ENEMY_SHIP_DIR, EXPLOSION_DIR


class Ship(pygame.sprite.Sprite):
    def __init__(
        self,
        pos: tuple[int, int],
        ship_type: ShipTypes,
        visible_group: pygame.sprite.Group,
        base_group: pygame.sprite.Group,
        bullet_group: pygame.sprite.Group,
    ):
        super().__init__((base_group, visible_group, bullet_group))

        self.frame_index = 0
        self.animation_speed = 0.25
        self.animations_list = load_frames(Ship.select_ship(ship_type))
        self.animations_list["dead"] = load_frame(EXPLOSION_DIR)
        self.direction = pygame.math.Vector2(0, 0)
        self.status = Status()

        self.image = self.animations_list[self.get_status()][0]
        self.rect = self.image.get_rect(topleft=pos)

        self.speed = 4

        self.bullet_group = bullet_group
        self.visible_group = visible_group

        self.cooldown = 200
        self.cooldown_timer = Cooldown(self.cooldown)

    @classmethod
    def select_ship(cls, ship_type: ShipTypes):
        ship = PLAYER_SHIP_DIR
        type_index = random.choice(["1", "2", "3"])
        if ship_type == ShipTypes.SHOOTING_ENEMY:
            ship = ENEMY_SHIP_DIR / ("shooter" + type_index)
        elif ship_type == ShipTypes.SELF_KILL_ENEMY:
            ship = ENEMY_SHIP_DIR / ("self_kill_" + type_index)
        return ship

    def animate(self):
        animation = self.get_current_animation()
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        frame_index = int(self.frame_index)
        self.image = animation[frame_index]
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def get_current_animation(self):
        return self.animations_list[self.get_status()]

    def update(self, *args, **kwargs):
        self.manage_status()
        self.animate()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def manage_status(self):
        if self.status == State.DEAD:
            return
        if self.direction.x != 0:
            self.status.set_state(State.MOVEMENT)
        else:
            self.status.set_state(State.IDLE)

    def get_status(self):
        if not self.status.is_dead():
            status = self.status.get_status()
            new_state = "idle"
            if status == State.MOVEMENT:
                if self.direction.x < 0:
                    new_state = "left"
                else:
                    new_state = "right"
            return new_state
        return "dead"
