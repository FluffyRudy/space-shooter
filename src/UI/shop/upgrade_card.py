from typing import Optional, Callable
import pygame, copy, math
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UILabel, UIImage, UIAutoResizingContainer
from pygame_gui.core import ObjectID, UIContainer
from src.storage.storage import Storage
from src.utils.image_util import load_frame
from src.settings import G_SPRITE_SIZE
from config import GRAPHICS_DIR


class UpgradeCard(UIAutoResizingContainer):
    button_to_upgrade_info: dict[UIButton, tuple[list[UIButton], Callable]] = {}

    def __init__(
        self,
        key: str,
        upgrade_type: str,
        relative_rect: pygame.Rect,
        manager: UIManager,
        container: Optional[UIContainer] = None,
    ):
        super().__init__(
            relative_rect=relative_rect,
            object_id=ObjectID(object_id="#upgradecard"),
            anchors={"top": "top", "centerx": "centerx"},
            manager=manager,
            container=container,
        )

        self.data = copy.deepcopy(Storage.get_game_data()[key][upgrade_type])
        self.upgrade_data = self.data["upgrades"]
        self.upgradable_labels = self.upgrade_data.get("upgradable")
        self.manager = manager
        self.key = key
        self.upgrade_type = upgrade_type
        self.cost_label = None

        self._setup_ui()

    @classmethod
    def set_coin_ui_callback(cls, callback: Callable):
        cls.update_coin_ui = callback

    @classmethod
    def get_upgrade_buttons(cls) -> dict[str, tuple[list[UIButton], Callable]]:
        return cls.button_to_upgrade_info

    def _setup_ui(self):
        OFFSET = 10
        surface = load_frame(GRAPHICS_DIR / "powerops" / self.upgrade_type)[0]

        title = self._create_title()
        image = self._create_image(surface, title)
        self._create_upgrade_labels(image, title, OFFSET)

    def _create_title(self) -> UILabel:
        offset_x = 10
        return UILabel(
            text=self.upgrade_type.capitalize(),
            relative_rect=pygame.Rect(G_SPRITE_SIZE + offset_x, 0, -1, -1),
            manager=self.manager,
            container=self,
            anchors={"top": "top", "left": "left"},
            object_id=ObjectID(object_id="#cardtitle"),
        )

    def _create_image(self, surface: pygame.Surface, title: UILabel) -> UIImage:
        return UIImage(
            relative_rect=pygame.Rect(
                (0, title.relative_rect.bottom),
                (G_SPRITE_SIZE, G_SPRITE_SIZE),
            ),
            image_surface=surface,
            manager=self.manager,
            container=self,
        )

    def _create_upgrade_labels(self, image: UIImage, title: UILabel, OFFSET: int):
        font_size = 20
        y_offset = len(self.upgradable_labels) * font_size
        pos_x = image.relative_rect.right + OFFSET
        pos_y = title.relative_rect.bottom

        for label_text in self.upgradable_labels:
            label = UILabel(
                relative_rect=pygame.Rect(pos_x, pos_y, -1, -1),
                text=label_text,
                manager=self.manager,
                container=self,
                object_id=ObjectID(object_id="#upgfont"),
            )
            self._create_upgrade_buttons(
                pos_x + G_SPRITE_SIZE * 3, pos_y, OFFSET, label_text
            )
            pos_y += y_offset + OFFSET

        self.cost_label = UILabel(
            relative_rect=pygame.Rect(pos_x, pos_y, -1, -1),
            text=f"COST: {self.upgrade_data.get('cost')}",
            manager=self.manager,
            container=self,
            object_id=ObjectID(object_id="#upgfont"),
        )
        image.set_relative_position(
            (image.relative_rect.left + 5, (pos_y - image.relative_rect.height) // 2)
        )

    def _create_upgrade_buttons(
        self, pos_x: int, pos_y: int, OFFSET: int, upgrade_type: str
    ):
        size = 25
        hint_buttons: list[UIButton] = []
        upgrade_index = self.upgradable_labels.index(upgrade_type)

        for btn_index in range(self.upgrade_data["max_upgrade_level"]):
            button_id = (
                "#active"
                if btn_index < self.upgrade_data["upgrade_level"][upgrade_index]
                else "#inactive"
            )
            upgrade_hint_button = UIButton(
                relative_rect=pygame.Rect(pos_x, pos_y, size, size),
                manager=self.manager,
                container=self,
                text="",
                object_id=ObjectID(object_id=button_id),
            )
            hint_buttons.append(upgrade_hint_button)
            pos_x += size + OFFSET

        upgrade_button = UIButton(
            relative_rect=pygame.Rect(pos_x, pos_y, -1, -1),
            manager=self.manager,
            container=self,
            text="+",
        )
        setattr(upgrade_button, "upgrade_type", upgrade_type)

        upgrade_button.set_relative_position(
            (
                upgrade_button.relative_rect.left,
                pos_y - (upgrade_button.relative_rect.height) // 4,
            )
        )
        UpgradeCard.button_to_upgrade_info[upgrade_button] = (
            hint_buttons,
            self.apply_upgrade,
        )

    def apply_upgrade(self, target_button: UIButton):
        upgrade_type = getattr(target_button, "upgrade_type")
        upgrade_index = self.upgradable_labels.index(upgrade_type)
        upgrade_data = self.data["upgrades"]
        current_level = upgrade_data["upgrade_level"][upgrade_index]
        avilable_coins = Storage.get_player_data()["coins"]

        if (
            current_level >= upgrade_data["max_upgrade_level"]
            or avilable_coins < upgrade_data["cost"]
        ):
            print("max reached or few coins")
            return

        upgrade_data["upgrade_level"][upgrade_index] += 1
        upgrade_data["cost"] += upgrade_data["cost_increase"]
        self.data[upgrade_type] = math.ceil(
            self.data[upgrade_type] * upgrade_data["power_increase_rate"]
        )

        new_coin_balance = avilable_coins - upgrade_data["cost"]

        Storage.write_upgrade_data(self.key, self.upgrade_type, self.data)
        Storage.write_player_data({"coins": new_coin_balance})
        self.activate_upgrade_hint(
            self.button_to_upgrade_info[target_button][0][current_level]
        )
        self.update_coin_ui(f"Coins: {new_coin_balance}")

        self.update_cost_label()

    def activate_upgrade_hint(self, hint_button: UIButton):
        hint_button.change_object_id(ObjectID(object_id="#active"))

    def update_cost_label(self):
        self.cost_label.set_text(f"COST: {self.upgrade_data.get('cost')}")
