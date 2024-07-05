import pygame, random
from .animation import Animation
from src.utils.image_util import load_frame
from src.sprites.weapons.laser import Laser
from src.settings import WIDTH, HEIGHT, G_SPRITE_SIZE
from config import POWEROPS_DIR


def get_power_path(type_: str):
    power_map = {"laser": POWEROPS_DIR / "laser"}
    power = random.choice(list(power_map.keys()))
    return power_map[power]


class Powerops(pygame.sprite.Sprite):
    def __init__(
        self,
        power_type: str,
        base_group: pygame.sprite.Group,
        visible_group: pygame.sprite.Group,
        action_group: pygame.sprite.Group,
    ):
        super().__init__([base_group, visible_group])
        self.action_group = action_group
        self.visible_group = visible_group

        self.power_type = power_type

        pos = random.randint(0, WIDTH - G_SPRITE_SIZE), random.randint(
            -G_SPRITE_SIZE, -G_SPRITE_SIZE // 2
        )
        size = (G_SPRITE_SIZE, G_SPRITE_SIZE)
        frames = load_frame(get_power_path(power_type), (0.5, 0.4))
        self.animation = Animation(frames)
        self.image = self.animation.initial_frame
        self.rect = self.image.get_rect(topleft=pos)
        self.fall_velocity = +3

    def update(self, *args, **kwargs):
        relative_rect = kwargs.get("player").rect
        self.rect.y += self.fall_velocity
        if self.rect.y >= HEIGHT or self.rect.colliderect(relative_rect):
            self.assign_power()
            self.kill()
        self.animation.animate()

    def assign_power(self):
        if self.power_type == "laser":
            Laser([self.visible_group, self.action_group], self.rect.midtop)
