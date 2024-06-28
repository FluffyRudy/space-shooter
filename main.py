import pygame, sys
from src.storage.storage import Storage
from src.level import Level
from src.utils.math_util import calculate_center
from src.settings import FPS, WIDTH, HEIGHT, BLACK

from src.UI.menu.gameover import GameoverUI


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level(level=Storage.get_current_level())
        self.gameoverUI = GameoverUI(calculate_center(self.screen.get_size()))

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Storage.write_current_level(self.level.current_level)
                sys.exit()

    def update(self):
        self.screen.fill(BLACK)
        self.handle_event()

        if False:
            self.level.run()
            if self.level.completed():
                self.level = Level(self.level.current_level + 1)
        else:
            self.gameoverUI.display(self.screen)

        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        while True:
            self.update()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
