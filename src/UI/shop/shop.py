from typing import Tuple
import pygame, pygame_gui
from pathlib import Path
from .entry import Entry
from src.settings import WIDTH, G_SPRITE_SIZE


class ShopManager(pygame_gui.UIManager):
    def __init__(self, size: Tuple[int, int]):
        theme_path = Path(__file__).resolve().parent / "theme.json"
        super().__init__(size, theme_path)
        self.entry_provider = Entry(
            pygame.Rect(
                WIDTH - G_SPRITE_SIZE * 3,
                G_SPRITE_SIZE * 2,
                G_SPRITE_SIZE * 2,
                G_SPRITE_SIZE,
            ),
            "S H O P",
            self,
        )

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.entry_provider:
                print("provided")
