import pygame
from typing import Union
from collections import deque
from src.animation.Text.fadeout import Fadeout


class NotificationManager:
    instance = None

    def __init__(self):
        if NotificationManager.instance is not None:
            return
        self.queue: deque[Union[Fadeout]] = deque()
        NotificationManager.instance = self

    def add(self, item: Union[Fadeout]):
        self.queue.append(item)

    def manage(self):
        if not self.queue:
            return
        for notification in self.queue:
            notification.update()
        if self.queue and self.queue[0].is_removable():
            self.queue.popleft()

    def draw(self, display_surface: pygame.Surface):
        if not self.queue:
            return
        for notification in self.queue:
            notification.display(display_surface)
