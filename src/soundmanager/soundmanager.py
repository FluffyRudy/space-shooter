from typing import Literal
import pygame
from config import SOUND_PATH


class SoundManager:
    LOOP = 1
    NO_LOOP = -1
    BG_SOUND = SOUND_PATH / "menu.mp3"
    SHOOT_SOUND = SOUND_PATH / "shoot.mp3"
    ENEMY_DAMAGE_SOUND = ""
    PLAYER_DAMAGE_SOUND = ""
    PICK_SOUND = ""
    GAMEOVER_SOUND = ""
    WIN_SOUND = ""

    def __init__(self):
        pygame.mixer.init()

        self.bg_sound = pygame.mixer.Sound(str(SoundManager.BG_SOUND))
        self.main_channel_sounds = {}
        self.sfx_sounds = {"shoot": pygame.mixer.Sound(SoundManager.SHOOT_SOUND)}
        self.bg_sound_loop = SoundManager.LOOP

        self.main_channel = pygame.mixer.Channel(1)
        self.sfx_channel = pygame.mixer.Channel(2)

    def set_main_channel_loop(self, to_loop: bool):
        self.bg_sound_loop = SoundManager.LOOP if to_loop else SoundManager.NO_LOOP

    def play_main_channel(self):
        self.main_channel.play(self.bg_sound, loops=self.bg_sound_loop)

    def pause_main_channel(self):
        self.main_channel.pause()

    def stop_main_channel(self):
        self.main_channel.stop()

    def update_bg_sound(self, sound_path: str):
        self.stop_main_channel()
        self.bg_sound = pygame.mixer.Sound(sound_path)
        self.play_main_channel()

    def play_sfx_sound(
        self,
        sound_type: Literal[
            "shoot", "enemydmg", "playerdmg", "pick", "gameover", "win"
        ],
    ):
        self.sfx_channel.stop()
        self.sfx_channel.play(self.sfx_sounds[sound_type])


Soundmanager = SoundManager()
