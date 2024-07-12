from typing import Optional, Callable
import pygame, copy
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UILabel, UIImage, UIAutoResizingContainer
from pygame_gui.core import ObjectID, UIContainer
from src.storage.storage import Storage
from src.utils.image_util import load_frame
from src.settings import G_SPRITE_SIZE
from config import GRAPHICS_DIR


class UpgradeCard(UIAutoResizingContainer):
    button_map: dict[UIButton, tuple[list[UIButton], Callable]] = {}

    def __init__(
        self,
        key: str,
        type_: str,
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
        self.upgrade_data = copy.deepcopy(
            Storage.get_game_data()[key][type_]["upgrades"]
        )
        self.upgradable_labels = self.upgrade_data.get("upgradable")
        self.manager = manager
        self.key = key
        self.type_ = type_

        self._setup_ui()

    @classmethod
    def get_upgrade_buttons(cls) -> dict[str, tuple[list[UIButton], Callable]]:
        return cls.button_map

    def _setup_ui(self):
        OFFSET = 10
        surface = load_frame(GRAPHICS_DIR / "powerops" / self.type_)[0]

        title = self._create_title()
        image = self._create_image(surface, title)
        self._create_upgrade_labels(image, title, OFFSET)

    def _create_title(self) -> UILabel:
        offset_x = 10
        return UILabel(
            text=self.type_.capitalize(),
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

        label = UILabel(
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

        for btn_icount in range(self.upgrade_data["max_upgrade_level"]):
            upg_hint_btn = UIButton(
                relative_rect=pygame.Rect(pos_x, pos_y, size, size),
                manager=self.manager,
                container=self,
                text="",
                object_id=ObjectID(
                    object_id=(
                        "#active"
                        if btn_icount
                        < self.upgrade_data["upgrade_level"][upgrade_index]
                        else "#inactive"
                    )
                ),
            )
            hint_buttons.append(upg_hint_btn)
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
        UpgradeCard.button_map[upgrade_button] = (hint_buttons, self.make_upgrade)

    def make_upgrade(self, target_btn: UIButton):
        upgrade_type = getattr(target_btn, "upgrade_type")
        upgrade_index = self.upgradable_labels.index(upgrade_type)
        new_data = self.upgrade_data

        upgrade_level = new_data["upgrade_level"][upgrade_index]
        new_data["upgrade_level"][upgrade_index] += 1
        new_data["cost"] = int(new_data["cost"] * new_data["cost_increase_rate"])

        Storage.write_upgrade_data(self.key, self.type_, new_data)
        self.active_upgrade_hint(self.button_map[target_btn][0][upgrade_level])

    def active_upgrade_hint(self, hint_btn: UIButton):
        hint_btn.change_object_id(ObjectID(object_id="#active"))
