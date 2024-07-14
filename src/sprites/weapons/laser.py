from typing import Union
import pygame
from src.storage.storage import Storage
from src.soundmanager.soundmanager import Soundmanager
from src.utils.image_util import load_frame
from src.timer.cooldown import Cooldown
from src.settings import HEIGHT
from config import WEAPONS_DIR


class Laser(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        pos: tuple[int, int],
    ):
        LASER_DIR = WEAPONS_DIR / "laser"
        ATTRIBUTES = Storage.get_weapons("laser")
        super().__init__(groups)
        self.damage = ATTRIBUTES.get("damage")
        self.frames = load_frame(LASER_DIR, (0.5, 1))
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.frames[0]

        self.rect = self.image.get_rect(
            midtop=(pos[0], pos[1] - self.image.get_height() * 0.97)
        )
        self.self_kill_cd = Cooldown(ATTRIBUTES.get("kill_after"))
        self.self_kill_cd.reset_time()
        Soundmanager.play_sfx_sound("laser", channel=4)

    def get_damage(self):
        return self.damage

    def animate(self):
        self.frame_index += self.animation_speed
        frame_index = int(self.frame_index) % len(self.frames)
        self.image = self.frames[frame_index]

    def update(self, *arg, **kwargs):
        relative_rect = kwargs.get("player").rect
        self.rect.centerx = relative_rect.centerx
        self.rect.top = relative_rect.y - self.image.get_height() * 0.99
        self.animate()
        self.self_kill_cd.handle_cooldown()
        self.handle_kill()

    def handle_kill(self):
        if self.self_kill_cd.has_cooldown():
            Soundmanager.stop_channel(channel=4)
            self.kill()
