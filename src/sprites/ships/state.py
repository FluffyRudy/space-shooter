import pygame, enum


class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class State(enum.Enum):
    IDLE = 0
    MOVEMENT = 1
    ATTACK = 2
    DEAD = 3


class Status:
    def __init__(self):
        self.status = State.IDLE

    def get_state(self):
        return self.status

    def is_idle(self):
        return self.status == State.IDLE

    def is_moving(self):
        return self.status == State.MOVEMENT

    def is_attacking(self):
        return self.status == State.ATTACK

    def is_dead(self):
        return self.status == State.DEAD

    def set_state(self, state: State):
        self.status = state
