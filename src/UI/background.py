import pygame
from pathlib import Path
from random import choice
from src.utils.image_util import load_frame
from config import UI_DIR


class Background:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.bg_frames = self.get_random_spaceBG()
        self.background_image = self.bg_frames[0]
        self.animation_speed = 0.1
        self.frame_index = 0

    def get_random_spaceBG(self):
        space_bg_dir = UI_DIR / "space_bg"
        return load_frame(choice(list(space_bg_dir.iterdir())), (4, 3))

    def draw_background(self, display_surface: pygame.Surface):
        display_surface.blit(self.background_image, (0, 0))

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.bg_frames):
            self.frame_index = 0
        frame_index = int(self.frame_index)
        self.background_image = self.bg_frames[frame_index]
