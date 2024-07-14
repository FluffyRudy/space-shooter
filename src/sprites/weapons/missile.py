import pygame
from src.soundmanager.soundmanager import Soundmanager
from .projectile import Projectile, create_projectile
from config import WEAPONS_DIR


class Missile(Projectile):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        pos: tuple[int, int],
        offset_coor: tuple[int, int],
        speed: float,
        direction: tuple[int, int],
        damage: int,
        sibling_offset_X,
    ):
        super().__init__(
            groups,
            pos,
            offset_coor,
            speed,
            direction,
            damage,
            WEAPONS_DIR / "missile",
            sibling_offset_X,
        )
        Soundmanager.play_sfx_sound("missile", channel=4)

    def handle_kill(self):
        Soundmanager.stop_channel(channel=4)
        super().handle_kill()
