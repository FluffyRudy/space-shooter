import pygame
from pygame_gui.elements import UIButton
from pygame_gui.core import ObjectID
from pygame_gui import UIManager
from src.utils.image_util import load_image
from src.settings import G_SPRITE_SIZE
from config import UI_DIR


class Entry(UIButton):
    def __init__(self, relative_rect: pygame.Rect, label: str, manager: UIManager):
        super().__init__(
            relative_rect,
            label,
            manager,
            object_id=ObjectID(object_id="#entry"),
            tool_tip_text="Purchase Or Upgrade",
        )

    def handle_entry(self):
        pass

    def update(self, time_delta: float):
        super().update(time_delta)
