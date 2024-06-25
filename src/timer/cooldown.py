import pygame


class Cooldown:
    def __init__(self, cooldown_timer: int):
        self.start_timer = 0
        self.cooldown_timer = cooldown_timer
        self.finish_cooldown = True

    def handle_cooldown(self):
        current_timer = pygame.time.get_ticks()
        if (current_timer - self.start_timer) >= self.cooldown_timer:
            self.finish_cooldown = True
        else:
            self.finish_cooldown = False

    def has_cooldown(self):
        return self.finish_cooldown

    def update_cooldown(self, new_cooldown):
        self.cooldown_timer = new_cooldown

    def reset_time(self):
        self.start_timer = pygame.time.get_ticks()
