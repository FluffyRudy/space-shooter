import pygame, typing
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIPanel
from pygame_gui.core import ObjectID, UIContainer
from pygame_gui import UI_BUTTON_PRESSED


class ClosablePanel(UIPanel):
    def __init__(
        self,
        relative_rect: pygame.Rect,
        manager: UIManager,
        container: typing.Optional[UIContainer] = None,
        object_id: typing.Optional[str] = None,
        anchors: typing.Optional[dict[str, str]] = {"center": "center"},
    ):
        super().__init__(
            relative_rect=relative_rect,
            manager=manager,
            object_id=ObjectID(object_id=object_id),
            container=container,
            anchors=anchors,
        )

        self.close_button = UIButton(
            relative_rect=pygame.Rect((-10, 0), (-1, -1)),
            text="🗴",
            manager=manager,
            container=self,
            anchors={"top": "top", "left": "right"},
            object_id=ObjectID(object_id="#close"),
        )
