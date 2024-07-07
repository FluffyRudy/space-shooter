import pygame, random
from .animation import Animation
from src.storage.storage import Storage
from src.utils.image_util import load_frame
from src.sprites.weapons.projectile import create_projectile
from src.sprites.weapons.laser import Laser
from src.sprites.weapons.missile import Missile
from src.sprites.defence.healthregan import HealthRegan
from src.sprites.defence.shield import Shield
from src.settings import WIDTH, HEIGHT, G_SPRITE_SIZE
from config import POWEROPS_DIR


def get_power_path(type_: str):
    power_map = {
        "laser": POWEROPS_DIR / "laser",
        "regan": POWEROPS_DIR / "health",
        "missile": POWEROPS_DIR / "missile",
        "shield": POWEROPS_DIR / "shield",
    }
    return power_map[type_]


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

        pos = random.randint(int(WIDTH // 4), int(WIDTH * 0.7)), random.randint(
            -G_SPRITE_SIZE, -G_SPRITE_SIZE // 2
        )
        size = (G_SPRITE_SIZE, G_SPRITE_SIZE)
        frames = load_frame(
            get_power_path(power_type), None, (G_SPRITE_SIZE // 2, G_SPRITE_SIZE // 2)
        )
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
        self.image = self.animation.get_current_frame()

    def assign_power(self):
        if self.power_type == "laser":
            Laser(self.get_filtered_group(), self.rect.midtop)
        elif self.power_type == "regan":
            HealthRegan(self.get_filtered_group(), self.rect.center)
        elif self.power_type == "shield":
            Shield(self.get_filtered_group(), self.rect.center)
        elif self.power_type == "missile":
            create_projectile(
                self.get_filtered_group(),
                self.rect,
                Storage.get_weapons("missile").get("count"),
                Storage.get_weapons("missile").get("speed"),
                Storage.get_weapons("missile").get("damage"),
                (0, -1),
                Missile,
            )

    def get_filtered_group(self) -> list:
        if self.action_group is None:
            return [self.visible_group]
        return [self.visible_group, self.action_group]
