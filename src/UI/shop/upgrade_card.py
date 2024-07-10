from typing import Optional
import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIPanel, UIImage
from pygame_gui.core import ObjectID, UIContainer
from src.utils.image_util import load_frame
from config import UI_DIR


class UpgradeCard(UIPanel):
    def __init__(
        self,
        key: str,
        type_: str,
        relative_rect: pygame.Rect,
        manager: UIManager,
        container=None,
    ):
        super().__init__(
            relative_rect=relative_rect,
            object_id=ObjectID(object_id="#upgradecard"),
            anchors={"centerx": "centerx", "top": "top"},
            manager=manager,
        )
        surface = load_frame(UI_DIR / "powerops" / type_)[0]
        icon = UIImage(
            (0, 0),
            surface,
            manager,
            container=self,
            anchors={"left": "left", "top": "top"},
        )
