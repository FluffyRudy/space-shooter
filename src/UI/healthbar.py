import pygame
from src.utils.image_util import load_frame
from config import UI_DIR


class Healthbar:
    def __init__(self, health_count: int):
        self.empty_health_chunks = load_frame(UI_DIR / "health" / "empty")
        self.filled_health_chunks = load_frame(UI_DIR / "health" / "filled")
        self.chunk_width = self.empty_health_chunks[0].get_width()
        self.health_count = health_count
        self.full_health = health_count

    def update_health_count(self, health_count: int):
        self.health_count = health_count

    def update(self, health_count: int):
        self.update_health_count(health_count)

    def get_size(self):
        return pygame.math.Vector2(self.empty_health_chunks[0].size)

    def display(self, display_surface: pygame.Surface):
        i = 0
        for i in range(self.full_health):
            display_surface.blit(
                self.empty_health_chunks[1], ((i + 1) * self.chunk_width, 0)
            )

        for i in range(self.health_count):
            display_surface.blit(
                self.filled_health_chunks[1], ((i + 1) * self.chunk_width, 0)
            )
