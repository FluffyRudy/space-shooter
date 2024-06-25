from enum import Enum

FPS = 60
WIDTH = 1024
HEIGHT = 768

G_SPRITE_SIZE = 64  # general sprite size

# colors
BLACK = (0, 0, 0, 255)


DEFAULT_BULLET_SPEED = 4.0


# ship types
class ShipTypes(Enum):
    PLAYER = 0
    SHOOTING_ENEMY = 1
    SELF_KILL_ENEMY = 2
