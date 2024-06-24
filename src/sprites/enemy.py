import pygame
from ship import Ship


class Enemy(Ship):
    def __init__(self, pos: tuple[int, int], *groups):
        super().__init__(pos, groups)
