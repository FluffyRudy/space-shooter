from typing import Tuple
import pygame, pygame_gui
from pathlib import Path
from .entry import Entry
from .upgrade_card import UpgradeCard
from .upgrade_container import UpgradeContainer
from .custompanel import ClosablePanel
from src.storage.storage import Storage
from src.constants import LASER, MISSILE, SHIELD, REGAN
from src.settings import WIDTH, HEIGHT, G_SPRITE_SIZE


class ShopManager(pygame_gui.UIManager):
    def __init__(self, size: Tuple[int, int]):
        theme_path = Path(__file__).resolve().parent / "theme.json"
        super().__init__(size, theme_path)

        self.initialize_upgrade_field()
        self.initialize_upgrade_items()

    def initialize_upgrade_field(self):
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
        panel_rect = self.upgrade_panel.relative_rect
        self.upgrade_container = UpgradeContainer(
            relative_rect=(
                panel_rect.topleft,
                (panel_rect.width, panel_rect.height * 0.9),
            ),
            manager=self,
            container=self.upgrade_panel,
        )

        self.upgrade_panel.hide()
        self.close_button = self.upgrade_panel.close_button

    def initialize_upgrade_items(self):
        x, y = 0, self.close_button.rect.height
        width = self.upgrade_container.rect.width * 0.9
        init_height = G_SPRITE_SIZE

        for key in Storage.get_all_defence().keys():
            card_rect = self.load_card(
                "defence", key, pygame.Rect((x, y), (width, init_height))
            )
            y = card_rect.bottom + card_rect.height // 4

        for key in Storage.get_all_weaponse().keys():
            card_rect = self.load_card(
                "weapons", key, pygame.Rect((x, y), (width, init_height))
            )
            y = card_rect.bottom + card_rect.height // 4

    def handle_events(self, event: pygame.event.Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.entry_provider:
                self.open_shop()
            elif event.ui_element == self.close_button:
                self.close_shop()

    def open_shop(self):
        self.entry_provider.hide()
        self.upgrade_panel.show()

    def close_shop(self):
        self.entry_provider.show()
        self.upgrade_panel.hide()

    def load_card(self, key: str, type_: str, rect: pygame.Rect):
        card = UpgradeCard(key, type_, rect, self, self.upgrade_container)
        return card.rect
