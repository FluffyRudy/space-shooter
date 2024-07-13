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
        self.isactive = False

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

        self.avilable_coins = Storage.get_player_data()["coins"]
        self.coin_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, 0, -1, -1),
            text="Coins: " + str(self.avilable_coins),
            manager=self,
            container=self.upgrade_panel,
            object_id=pygame_gui.core.ObjectID(object_id="#cardtitle"),
            anchors={"centerx": "centerx"},
        )

        self.upgrade_panel.hide()
        self.close_button = self.upgrade_panel.close_button

    def initialize_upgrade_items(self):
        UpgradeCard.set_coin_ui_callback(self.update_coinUI)

        x, y = 0, self.close_button.rect.height
        width = self.upgrade_container.rect.width * 0.9
        init_height = G_SPRITE_SIZE * 2.5

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
            for button, (upg_hint, action) in UpgradeCard.get_upgrade_buttons().items():
                if event.ui_element == button:
                    action(button)

    def update_coinUI(self, text: str):
        self.coin_label.set_text(text)

    def open_shop(self):
        self.entry_provider.hide()
        self.upgrade_panel.show()
        self.isactive = True

    def close_shop(self):
        self.entry_provider.show()
        self.upgrade_panel.hide()
        self.isactive = False

    def isopen(self):
        return self.isactive

    def load_card(self, key: str, type_: str, rect: pygame.Rect):
        card = UpgradeCard(key, type_, rect, self, self.upgrade_container)
        return card.rect
