import pygame, sys, time
from src.storage.storage import Storage
from src.level import Level
from src.UI.menu.mainmenu import MainMenuUI
from src.UI.menu.gameover import GameoverUI
from src.settings import FPS, WIDTH, HEIGHT, BLACK


class Manager:
    def __init__(self):
        pygame.init()

        self.quit_game = False
        self.start_game = False
        self.event = None

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.level = Level(level=Storage.get_current_level())

        self.gameover = GameoverUI(
            (WIDTH // 2, HEIGHT // 2),
            {
                "close": lambda: self.end_game(),
                "replay": lambda: self.replay(),
                "main_menu": lambda: print("main_menu"),
            },
        )
        self.mainmenu = MainMenuUI(
            (WIDTH // 2, HEIGHT // 2),
            {
                "play": lambda: print("start"),
                "replay": lambda: print("levels"),
                "close": lambda: print("main_menu"),
            },
        )

    def handle_event(self):
        self.event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True
            self.event = event

        if self.quit_game:
            Storage.write_current_level(self.level.current_level)
            sys.exit()

    def replay(self):
        self.level.is_gameover = False
        self.level = Level(self.level.current_level)

    def end_game(self):
        self.quit_game = True

    def update(self):
        self.screen.fill(BLACK)
        self.handle_event()

        if self.level.is_gameover:
            self.gameover.display(self.screen)
            self.gameover.update(self.event)
        elif self.start_game:
            self.level.run(self.event)
        else:
            self.mainmenu.display(self.screen)
            self.mainmenu.update(self.event)

        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        while True:
            self.update()
