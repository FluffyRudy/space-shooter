import pygame


class Cooldown:
    def __init__(self, cooldown_timer: int):
        """
        Initializes the Cooldown object with a specified cooldown timer.

        Args:
            cooldown_timer (int): The duration of the cooldown in milliseconds.
        """
        self.start_timer = 0
        self.cooldown_timer = cooldown_timer
        self.finish_cooldown = True

    def handle_cooldown(self) -> None:
        """
        Updates the cooldown status based on the elapsed time.
        """
        current_timer = pygame.time.get_ticks()
        if (current_timer - self.start_timer) >= self.cooldown_timer:
            self.finish_cooldown = True
        else:
            self.finish_cooldown = False

    def has_cooldown(self) -> bool:
        """
        Checks if the cooldown period has finished.

        Returns:
            bool: True if the cooldown period has finished, False otherwise.
        """
        return self.finish_cooldown

    def update_cooldown(self, new_cooldown: int) -> None:
        """
        Updates the cooldown timer with a new value.

        Args:
            new_cooldown (int): The new cooldown duration in milliseconds.
        """
        self.cooldown_timer = new_cooldown

    def reset_time(self) -> None:
        """
        Resets the start timer to the current time.
        """
        self.start_timer = pygame.time.get_ticks()
        self.finish_cooldown = False
