import pygame
from src.utils.image_util import load_frame
from config import UI_DIR


class CoinUI(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        self.frames = load_frame(UI_DIR / "coin")
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.coin = 0
        self.font = pygame.font.Font(None, self.image.get_size()[1] * 2)

        self.update_coin(0)

    def update_coin(self, amount: int):
        self.coin = amount
        self.text = self.font.render(f"{self.coin}", True, (255, 255, 255))

    def update(self, *args, **kwargs):
        self.animate()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def display(self, display_surface: pygame.Surface):
        display_surface.blit(
            self.image, (self.rect.left, self.rect.top + self.rect.height // 2)
        )
        display_surface.blit(
            self.text, (self.rect.right + 10, self.rect.y + self.rect.height // 2.2)
        )
