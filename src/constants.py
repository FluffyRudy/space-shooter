import pygame
from enum import Enum

MAX_SPAWN_COUNT = "max_spawn_count"
SPAWN_COUNT = "spawn_count"
ENEMIES = "enemies"
HEALTH_COUNT = "health_count"
SHOOTER = "shooter"
SELF_KILLER = "self_killer"
LASER = "laser"
REGAN = "regan"
MISSILE = "missile"
BULLET_SPEED = "bullet_speed"
BULLET_DAMAGE = "bullet_damage"
HEALTH = "health"
SHIELD = "shield"
AMOUNT = "amount"
KILL_AFTER = "kill_after"


class ShipTypes(Enum):
    PLAYER = 0
    SHOOTING_ENEMY = 1
    SELF_KILL_ENEMY = 2


class ObstacleTypes(Enum):
    ASTEROID = 0


class GlobalPos:
    parent_rect: pygame.Rect = None

    @classmethod
    def set_parent_rect(cls, rect: pygame.Rect):
        cls.parent_rect = rect


# colors
BLACK = (0, 0, 0, 255)
LIME = (0, 255, 0)
