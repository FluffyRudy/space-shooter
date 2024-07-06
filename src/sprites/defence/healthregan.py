from typing import Union
import pygame
from src.storage.storage import Storage
from src.utils.image_util import load_frame
from src.timer.cooldown import Cooldown
from src.settings import HEIGHT
from config import DEFENCE_DIR


class HealthRegan(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        pos: tuple[int, int],
    ):
        POWER_DIR = DEFENCE_DIR / "health"
        ATTRIBUTES = Storage.get_defence("regan")
        self.amount = ATTRIBUTES.get("amount")

        super().__init__(groups)
        self.frames = load_frame(POWER_DIR)
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.frames[0]

        self.rect = self.image.get_rect(center=pos)
        self.self_kill_cd = Cooldown(ATTRIBUTES.get("kill_after"))
        self.self_kill_cd.reset_time()

    def get_amount(self):
        return self.amount

    def animate(self):
        self.frame_index += self.animation_speed
        frame_index = int(self.frame_index) % len(self.frames)
        if frame_index == 0:
            self.frame_index = 0
        self.image = self.frames[frame_index]

    def update(self, *arg, **kwargs):
        kwargs.get("player").increase_health_count()
        self.rect.center = kwargs.get("player").rect.center

        self.animate()
        self.self_kill_cd.handle_cooldown()
        self.handle_kill()

    def handle_kill(self):
        if self.self_kill_cd.has_cooldown():
            self.kill()
