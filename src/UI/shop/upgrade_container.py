from typing import Optional
import pygame
from pygame_gui import UIManager
from pygame_gui.core import ObjectID, UIElement, UIContainer
from pygame_gui.elements import UIScrollingContainer
from src.utils.image_util import load_image
from config import UI_DIR


class UpgradeContainer(UIScrollingContainer):
    def __init__(
        self,
        relative_rect: pygame.Rect,
        manager: UIManager,
        container: Optional[UIContainer] = None,
    ):
        super().__init__(
            relative_rect=relative_rect,
            manager=manager,
            container=container,
            object_id=ObjectID(object_id="#upgradecontainer"),
            anchors={"center": "center"},
            allow_scroll_x=False,
        )
        self.set_scrollable_area_dimensions(self.rect.size)

    def add_upgrade_card(self, widget: UIElement):
        widget.set_container(self)
