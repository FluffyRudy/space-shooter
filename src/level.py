import pygame
from src.UI.background import Background
from .sprites.player import Player
from .settings import WIDTH, HEIGHT, G_SPRITE_SIZE


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.background = Background()

        self.visible_group = pygame.sprite.Group()
        self.player = Player(
            (WIDTH // 2 - G_SPRITE_SIZE // 2, HEIGHT - G_SPRITE_SIZE),
            self.visible_group,
        )

    def run(self):
        self.background.update()
        self.visible_group.update()
        self.background.draw_background(self.display_surface)
        self.visible_group.draw(self.display_surface)
