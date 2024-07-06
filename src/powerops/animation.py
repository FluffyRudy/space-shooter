import pygame


class Animation:
    def __init__(self, frames: list[pygame.Surface], animation_speed: float = 0.2):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.initial_frame

    @property
    def initial_frame(self):
        return self.frames[0]

    def get_current_frame(self):
        return self.image

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        print(self.frame_index)
