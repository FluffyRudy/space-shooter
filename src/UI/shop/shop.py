from typing import Tuple
import pygame, pygame_gui
from pathlib import Path
from .entry import Entry
from .upgrade_card import UpgradeCard
from .upgrade_container import UpgradeContainer
from .custompanel import ClosablePanel
from src.settings import WIDTH, HEIGHT, G_SPRITE_SIZE


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
        self.upgrade_panel = ClosablePanel(
            relative_rect=pygame.Rect(0, 0, WIDTH * 0.6, HEIGHT * 0.9),
            manager=self,
            object_id="#upgradepanel",
        )
        self.upgrade_container = UpgradeContainer(
            relative_rect=self.upgrade_panel.relative_rect,
            manager=self,
            container=self.upgrade_panel,
        )
        self.upgrade_panel.hide()

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.entry_provider:
                self.display_shop()

    def display_shop(self):
        self.entry_provider.hide()
        self.upgrade_panel.show()

    def close_shop(self):
        self.entry_provider.show()
        self.upgrade_panel.hide()
