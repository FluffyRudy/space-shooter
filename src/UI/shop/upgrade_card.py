from typing import Optional
import pygame
from pygame_gui import UIManager, TEXT_EFFECT_BOUNCE
from pygame_gui.elements import (
    UIButton,
    UIPanel,
    UIImage,
    UILabel,
    UIAutoResizingContainer,
)
from pygame_gui.core import ObjectID, UIContainer
from src.storage.storage import Storage
from src.utils.image_util import load_frame
from src.settings import G_SPRITE_SIZE
from config import GRAPHICS_DIR


class UpgradeCard(UIAutoResizingContainer):
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

        upgrade_data: dict = Storage.get_game_data()[key][type_]["upgrades"]
        upgradable_label: list = upgrade_data.get("upgradable")

        OFFSET = 10
        surface = load_frame(GRAPHICS_DIR / "powerops" / type_)[0]

        title = UILabel(
            text=type_.capitalize(),
            relative_rect=pygame.Rect(0, 0, -1, -1),
            manager=manager,
            container=self,
            anchors={"top": "top", "centerx": "centerx"},
            object_id=ObjectID(object_id="#cardtitle"),
        )
        image = UIImage(
            relative_rect=pygame.Rect(
                (0, title.relative_rect.bottom),
                (G_SPRITE_SIZE, G_SPRITE_SIZE),
            ),
            image_surface=surface,
            manager=manager,
            container=self,
        )

        font_size = 20
        y_offset = len(upgradable_label) * (font_size)
        pos_x = image.relative_rect.right + OFFSET
        pos_y = title.relative_rect.bottom

        for label in upgradable_label:
            label = UILabel(
                relative_rect=pygame.Rect(pos_x, pos_y, -1, -1),
                text=label,
                manager=manager,
                container=self,
                object_id=ObjectID(object_id="#upgfont"),
            )
            x = 300
            size = 25
            for btn_icount in range(upgrade_data["max_upgrade_level"]):
                UIButton(
                    relative_rect=pygame.Rect(x, pos_y, size, size),
                    manager=manager,
                    container=self,
                    text="",
                    object_id=ObjectID(
                        object_id=(
                            "#active"
                            if btn_icount < upgrade_data["upgrade_level"]
                            else "#inactive"
                        )
                    ),
                )
                x += size + OFFSET
            stats_btn = UIButton(
                relative_rect=pygame.Rect(x, pos_y, size * 2, size),
                manager=manager,
                container=self,
                text="+",
            )
            pos_y += y_offset

        image.set_relative_position(
            (image.relative_rect.left, (pos_y - image.relative_rect.top) // 2)
        )
