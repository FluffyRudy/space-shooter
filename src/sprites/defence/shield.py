from typing import Union
import pygame
from src.storage.storage import Storage
from src.utils.image_util import load_frame
from src.timer.cooldown import Cooldown
from src.constants import SHIELD, KILL_AFTER
from config import DEFENCE_DIR


class Shield(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        pos: tuple[int, int],
    ):
        super().__init__(groups)

        ATTRIBUTES = Storage.get_defence(SHIELD)
        self.frames = load_frame(DEFENCE_DIR / SHIELD, (0.3, 0.3))
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.self_kill_cd = Cooldown(ATTRIBUTES.get(KILL_AFTER))
        self.self_kill_cd.reset_time()

        self.bright_up_cd = Cooldown(200)
        self.is_brighten = False

        self.alpha_rate = 255 / ATTRIBUTES.get(KILL_AFTER)

    def animate(self):
        self.frame_index = (self.frame_index + self.animation_speed) % len(self.frames)
        if int(self.frame_index) == 0:
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, *arg, **kwargs):
        self.rect.center = kwargs.get("player").rect.center

        self.animate()
        self.self_kill_cd.handle_cooldown()
        self.handle_alpha()

        if self.self_kill_cd.has_cooldown():
            kwargs.get("player").make_vulnerable()
            self.kill()
        else:
            kwargs.get("player").make_immune()

    def handle_alpha(self):
        if self.is_brighten:
            self.bright_up_cd.handle_cooldown()
            if self.bright_up_cd.has_cooldown():
                self.is_brighten = False
        else:
            elapsed_time = self.self_kill_cd.get_prev_time()
            updated_alpha = max(80, 255 - self.alpha_rate * elapsed_time)
            self.image.set_alpha(int(updated_alpha))

    def bright_up(self):
        self.is_brighten = True
        self.bright_up_cd.reset_time()
        self.image.set_alpha(255)
