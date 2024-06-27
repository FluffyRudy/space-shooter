import pygame
from src.utils.image_util import load_frame
from config import HEALTH_UI_DIR


class Healthbar:
    def __init__(self, health_count: int):
        self.empty_health_chunks = load_frame(HEALTH_UI_DIR / "empty")
        self.filled_health_chunks = load_frame(HEALTH_UI_DIR / "filled")
        self.chunk_width = self.empty_health_chunks[0].get_width()
        self.health_count = health_count

    def update_health_count(self, health_count: int):
        self.health_count = health_count

    def display(self, display_surface: pygame.Surface):
        i = 0
        display_surface.blit(self.empty_health_chunks[0], (0, 0))
        for i in range(self.health_count):
            display_surface.blit(
                self.empty_health_chunks[1], ((i + 1) * self.chunk_width, 0)
            )
        display_surface.blit(
            pygame.transform.flip(self.empty_health_chunks[0], True, False),
            ((i + 1) * self.chunk_width, 0),
        )

        display_surface.blit(self.filled_health_chunks[0], (0, 0))
        for i in range(self.health_count):
            display_surface.blit(
                self.filled_health_chunks[1], ((i + 1) * self.chunk_width, 0)
            )
        display_surface.blit(
            pygame.transform.flip(self.filled_health_chunks[0], True, False),
            ((i + 1) * self.chunk_width, 0),
        )
