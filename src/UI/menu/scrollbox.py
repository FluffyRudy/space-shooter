from typing import Callable, Optional
import pygame
from src.utils.image_util import load_image
from src.UI.menu.button import CustomButton
from src.UI.menu.container import Container
from src.settings import HEIGHT, WIDTH, G_SPRITE_SIZE
from config import UI_DIR


class Scrollbox:
    def __init__(self, pos: tuple[int, int], box_callback: Callable[[str], None]):

        common_path = UI_DIR / "menu" / "common"
        size = int(WIDTH * 0.4), int(HEIGHT * 0.7)
        overlay_size = size[0] * 0.9, size[1] * 0.7
        self.image = load_image(common_path / "box.png", None, size)
        self.overlay = pygame.Surface(overlay_size, pygame.SRCALPHA)
        self.cancel_btn = load_image(
            common_path / "close.png", None, (G_SPRITE_SIZE, G_SPRITE_SIZE)
        )

        self.rect = self.image.get_rect(center=pos)
        self.cancel_btn_rect = self.cancel_btn.get_rect(topright=(self.rect.width, 0))
        self.action = box_callback
        self.is_visible = False

        self.cell_coor_y = 0
        self.levels_list: list[CustomButton] = []

    def set_cell_callback(self, callback: Callable[[str], None]):
        self.cell_callback = callback

    def make_visible(self):
        self.is_visible = True

    def extended_cell_callback(self, level: int):
        self.cell_callback(level)
        self.is_visible = False

    def add_cell(self, label: str):
        self.levels_list.append(
            CustomButton(
                label,
                (
                    self.rect.width // 2,
                    self.cell_coor_y * G_SPRITE_SIZE // 2
                    + self.cell_coor_y * G_SPRITE_SIZE
                    + G_SPRITE_SIZE // 2,
                ),
                lambda: self.extended_cell_callback(int(label)),
                size=(self.overlay.get_width() // 1.5, G_SPRITE_SIZE),
            )
        )
        self.cell_coor_y += 1

    def display(self, display_surface: pygame.Surface):
        if self.is_visible:
            if self.image.get_alpha() != 255:
                self.image.set_alpha(255)

            # Fill the entire image with black
            self.image.fill((0, 0, 0))

            # Draw the borders
            border_color = (255, 255, 255)  # Example border color
            border_thickness = 2  # Example border thickness

            # Top border
            self.image.fill(
                border_color, rect=(0, 0, self.image.get_width(), border_thickness)
            )
            # Bottom border
            self.image.fill(
                border_color,
                rect=(
                    0,
                    self.image.get_height() - border_thickness,
                    self.image.get_width(),
                    border_thickness,
                ),
            )
            # Left border
            self.image.fill(
                border_color, rect=(0, 0, border_thickness, self.image.get_height())
            )
            # Right border
            self.image.fill(
                border_color,
                rect=(
                    self.image.get_width() - border_thickness,
                    0,
                    border_thickness,
                    self.image.get_height(),
                ),
            )

            for level_btn in self.levels_list:
                # if level_btn.rect.top > self.cancel_btn_rect.height:
                level_btn.display(self.overlay)

            self.image.blit(self.cancel_btn, self.cancel_btn_rect.topleft)
            self.image.blit(
                self.overlay, (border_thickness, self.cancel_btn_rect.bottom + 1)
            )

            display_surface.blit(self.image, self.rect.topleft)

            self.overlay.fill((0, 0, 0))
        else:
            self.image.set_alpha(0)

    def update(self, event: Optional[pygame.event.Event]):
        if not self.is_visible:
            return

        if event.type == pygame.MOUSEWHEEL:
            self.handle_mousewheel(event)

        mouse_pos = pygame.mouse.get_pos()
        pos_x = max(0, mouse_pos[0] - self.rect.left)
        pos_y = mouse_pos[1] - self.rect.top

        if self.cancel_btn_rect.collidepoint((pos_x, pos_y)):
            self.handle_cancel_button(event)

        if event.type == pygame.MOUSEBUTTONUP:
            self.handle_cell_event((pos_x, pos_y))

    def handle_mousewheel(self, event):
        dir_y = event.dict.get("y")
        if dir_y == -1 and self.levels_list[-1].rect.bottom > self.overlay.get_height():
            self.scroll_levels(dir_y)
        elif dir_y == 1 and self.levels_list[0].rect.top < 0:
            self.scroll_levels(dir_y)

    def scroll_levels(self, dir_y):
        offset = (G_SPRITE_SIZE + 10) * dir_y
        for level_btn in self.levels_list:
            level_btn.rect.top += offset

    def handle_cell_event(self, pos: tuple[int, int]):
        position = pos[0], pos[1] - self.cancel_btn_rect.bottom
        for level_btn in self.levels_list:
            if level_btn.rect.collidepoint(position):
                level_btn.trigger_action()

    def handle_cancel_button(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.is_visible = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.cancel_btn = load_image(
                UI_DIR / "buttons" / "active" / "close.png",
                None,
                (G_SPRITE_SIZE, G_SPRITE_SIZE),
            )
