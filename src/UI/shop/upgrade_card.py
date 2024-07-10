from typing import Optional
import pygame, pygame_gui
from pygame_gui.core import ObjectID
from src.utils.image_util import load_image
from config import UI_DIR


class UpgradeCard(pygame_gui.elements.UIPanel):
    def __init__(
        self,
        icon_path: str,
        key: str,
        type_: str,
        relative_rect: pygame.Rect,
        manager: pygame_gui.UIManager,
        container=None,
    ):
        super().__init__(
            relative_rect=relative_rect,
            object_id=ObjectID(object_id="#upgradecard"),
            anchors={"centerx": "centerx", "top": "top"},
            manager=manager,
        )
