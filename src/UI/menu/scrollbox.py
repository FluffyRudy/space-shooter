from typing import Callable, Optional
import pygame
from src.utils.image_util import load_image
from src.UI.menu.button import CustomButton
from src.UI.menu.container import Container
from src.settings import HEIGHT, WIDTH, G_SPRITE_SIZE
from config import UI_DIR


class Scrollbox:
    def __init__(self, pos: tuple[int, int], callback: Callable[[str], None]):
        common_path = UI_DIR / "menu" / "common"
        size = int(WIDTH * 0.4), int(HEIGHT * 0.7)
        self.image = load_image(common_path / "box.png", None, size)
        self.cancel_btn = load_image(
            common_path / "close.png", None, (G_SPRITE_SIZE, G_SPRITE_SIZE)
        )
        self.rect = self.image.get_rect(center=pos)
        self.cancel_btn_rect = self.cancel_btn.get_rect(topright=(self.rect.width, 0))
        self.action = callback
        self.is_visible = False

    def make_visible(self):
        self.is_visible = True

    def add_cell(self, label: str):
        pass

    def display(self, display_surface: pygame.Surface):
        if self.is_visible:
            self.image.set_alpha(255)
            self.image.blit(self.cancel_btn, (self.cancel_btn_rect.topleft))
            display_surface.blit(self.image, self.rect.topleft)
        else:
            self.image.set_alpha(0)

    def update(self, event: Optional[pygame.event.Event]):
        if not self.is_visible:
            return
        mouse_pos = pygame.mouse.get_pos()
        pos_x = max(0, mouse_pos[0] - self.rect.left)
        pos_y = mouse_pos[1] - self.rect.top

        if (
            self.cancel_btn_rect.collidepoint((pos_x, pos_y))
            and event.type == pygame.MOUSEBUTTONUP
        ):
            self.is_visible = False
            print("sdf")
