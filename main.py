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

        self.level = Level(level=Storage.get_current_level())

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Storage.write_current_level(self.level.current_level)
                sys.exit()

    def update(self):
        self.screen.fill(BLACK)
        self.handle_event()

        self.level.run()
        if self.level.completed():
            self.level = Level(self.level.current_level + 1)
            print(self.level.current_level)

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
