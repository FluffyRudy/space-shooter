from typing import Optional
import pygame
from src.settings import WIDTH, HEIGHT
from config import FONT_DIR


class Fadeout:

    def __init__(
        self,
        text: str,
        size: int = 25,
        font: Optional[pygame.font.Font] = None,
        color: tuple[int, int, int, Optional[int]] = (255, 0, 0, 255),
    ):
        center_pos = (WIDTH // 2, HEIGHT // 2)
        font = pygame.font.Font(FONT_DIR / "NotoSansSymbols2-Regular.ttf", size)
        self.text_surf = font.render(text, True, color)
        self.rect = self.text_surf.get_rect(center=center_pos)
        self.border_rect = self.rect.inflate(20, 20)
        if isinstance(font, pygame.font.Font):
            self.font = font
        self.velocity = -5

    def update(self):
        self.rect.y += self.velocity
        self.border_rect.y += self.velocity

    def is_removable(self):
        return self.rect.y <= 50

    def display(self, display_surface: pygame.Surface):
        pygame.draw.rect(display_surface, (255, 255, 255), self.border_rect, 2, 5)
        display_surface.blit(self.text_surf, self.rect.topleft)
