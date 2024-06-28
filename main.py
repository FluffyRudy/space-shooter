import pygame, sys
from src.storage.storage import Storage
from src.level import Level
from src.settings import FPS, WIDTH, HEIGHT, BLACK
from src.storage.storage import StorageHandler


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level(level=1)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def update(self):
        self.screen.fill(BLACK)
        self.handle_event()

        self.level.run()
        if self.level.completed():
            self.level = Level(2)

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
