from typing import Literal
import pygame
from config import SOUND_PATH


class SoundManager:
    """
    A class to manage sound effects and background music using Pygame.

    Attributes:
        LOOP (int): Constant representing looping playback.
        NO_LOOP (int): Constant representing non-looping playback.
        BG_SOUND (str): Path to the background music file.
        SHOOT_SOUND (str): Path to the shoot sound effect file.
        ENEMY_DESTROY_SOUND (str): Path to the enemy destroy sound effect file.
        OBSTACLE_DESTROY_SOUND (str): Path to the obstacle destroy sound effect file.
        PLAYER_DAMAGE_SOUND (str): Placeholder for player damage sound effect path.
        PICK_SOUND (str): Placeholder for pick sound effect path.
        GAMEOVER_SOUND (str): Placeholder for game over sound effect path.
        WIN_SOUND (str): Placeholder for win sound effect path.
    """

    LOOP = -1
    NO_LOOP = 1
    BG_SOUND = SOUND_PATH / "main-sound.mp3"
    SHOOT_SOUND = SOUND_PATH / "shoot.mp3"
    LASER_SOUND = SOUND_PATH / "laser.ogg"
    ENEMY_DESTROY_SOUND = SOUND_PATH / "ship-destroy.mp3"
    OBSTACLE_DESTROY_SOUND = SOUND_PATH / "ship-destroy.mp3"
    PLAYER_DAMAGE_SOUND = ""
    PICK_SOUND = ""
    GAMEOVER_SOUND = ""
    WIN_SOUND = ""

    def __init__(self):
        """
        Initializes the SoundManager with Pygame mixer and loads initial sound files.
        """
        pygame.mixer.init()
        self.bg_sound = pygame.mixer.Sound(str(SoundManager.BG_SOUND))
        self.sfx_sounds = {
            "shoot": pygame.mixer.Sound(str(SoundManager.SHOOT_SOUND)),
            "laser": pygame.mixer.Sound(str(SoundManager.LASER_SOUND)),
            "enemy_destroy": pygame.mixer.Sound(str(SoundManager.ENEMY_DESTROY_SOUND)),
            "obstacle_destroy": pygame.mixer.Sound(
                str(SoundManager.OBSTACLE_DESTROY_SOUND)
            ),
        }
        self.bg_sound_loop = SoundManager.LOOP

        self.main_channel = pygame.mixer.Channel(1)
        self.sfx_channel_0 = pygame.mixer.Channel(2)
        self.sfx_channel_1 = pygame.mixer.Channel(3)
        self.sfx_channel_2 = pygame.mixer.Channel(4)

    def set_channel_intensity(self, channel: Literal[1, 2, 3], intensity: float):
        """
        Sets the intensity (volume) of the sound effects channel.

        Args:
            channel (Literal[1, 2, 3]): The channel number to set intensity for.
            intensity (float): The intensity level between 0.0 (silent) and 1.0 (full volume).

        Raises:
            ValueError: If intensity is not between 0 and 1.

        Note:
            Avoid misuse of `main_channel` and refrain from modifying it directly if possible,
            as it is reserved for controlling the background music playback.
        """
        if not 0 <= intensity <= 1:
            raise ValueError("Intensity must be between 0 and 1")

        if channel == 1:
            self.main_channel.set_volume(intensity)
        elif channel == 2:
            self.sfx_channel_0.set_volume(intensity)
        elif channel == 3:
            self.sfx_channel_1.set_volume(intensity)

    def set_main_channel_loop(self, to_loop: bool):
        """
        Sets whether the background music should loop or not.

        Args:
            to_loop (bool): True to loop the background music, False otherwise.
        """
        self.bg_sound_loop = SoundManager.LOOP if to_loop else SoundManager.NO_LOOP

    def play_main_channel(self):
        """
        Plays the background music on the main channel with looping settings.
        """
        self.main_channel.play(self.bg_sound, loops=self.bg_sound_loop)

    def pause_main_channel(self):
        """
        Pauses the playback of the background music on the main channel.
        """
        self.main_channel.pause()

    def stop_main_channel(self):
        """
        Stops the playback of the background music on the main channel.
        """
        self.main_channel.stop()

    def stop_channel(self, channel: Literal[1, 2, 3, 4]):
        if channel == 1:
            self.main_channel.stop()
        elif channel == 2:
            self.sfx_channel_0.stop()
        elif channel == 3:
            self.sfx_channel_1.stop()
        elif channel == 4:
            self.sfx_channel_2.stop()

    def update_bg_sound(self, sound_path: str):
        """
        Updates the background music with a new sound file path and replays it.

        Args:
            sound_path (str): The new path to the background music sound file.
        """
        self.stop_main_channel()
        self.bg_sound = pygame.mixer.Sound(sound_path)
        self.play_main_channel()

    def play_sfx_sound(
        self,
        sound_type: Literal["shoot", "laser", "enemy_destroy", "obstacle_destroy"],
        channel: Literal[2, 3, 4] = 2,
    ):
        """
        Plays a specified sound effect on the selected channel.

        Args:
            sound_type (Literal["shoot", "enemy_destroy", "obstacle_destroy"]): The type of sound effect to play.
            channel (Literal[2, 3], optional): The channel number to play the sound effect on. Defaults to 2.
        """
        if channel == 2:
            self.sfx_channel_0.stop()
            self.sfx_channel_0.play(self.sfx_sounds[sound_type])
        elif channel == 3:
            self.sfx_channel_1.stop()
            self.sfx_channel_1.play(self.sfx_sounds[sound_type])
        elif channel == 4:
            self.sfx_channel_2.stop()
            self.sfx_channel_2.play(self.sfx_sounds[sound_type], loops=self.LOOP)


Soundmanager = SoundManager()
