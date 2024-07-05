import pygame


class Animation:
    def __init__(self, frames: list[pygame.Surface], animation_speed: float = 0.2):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = animation_speed

    @property
    def initial_frame(self):
        return self.frames[0]

    def animate(self):
        self.frame_index += self.animation_speed
        frame_index = int(self.frame_index) % len(self.frames)
        self.image = self.frames[frame_index]
