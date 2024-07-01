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
                "main_menu": lambda: self.return_menu(),
            },
        )
        # main menu has levels option that is binded with main menu itself
        self.mainmenu = MainMenuUI(
            (WIDTH // 2, HEIGHT // 2),
            {
                "play": lambda: self.play(),
                "load_level": lambda level: self.load_level(level),
                "exit": lambda: self.end_game(),
            },
        )

    def handle_event(self):
        self.event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True
                Storage.write_current_level(self.level.current_level)
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.MOUSEBUTTONUP
                or event.type == pygame.MOUSEWHEEL
            ):
                self.event = event

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.return_menu()

        if self.quit_game:
            Storage.write_current_level(
                max(Storage.get_current_level(), self.level.current_level)
            )
            sys.exit()

    def replay(self):
        self.level.is_gameover = False
        self.level = Level(self.level.current_level)

    def end_game(self):
        self.quit_game = True

    def play(self):
        self.start_game = True

    def return_menu(self):
        self.start_game = False

    def load_level(self, level: int):
        print(level)
        self.level = Level(level)
        self.play()

    def update(self):
        self.handle_event()

        if self.start_game:
            self.level.run(self.event)
            if self.level.is_gameover:
                self.gameover.display(self.screen)
                self.gameover.update(self.event)
            elif self.level.completed():
                self.load_level(self.level.current_level + 1)
                Storage.write_current_level(self.level.current_level + 1)
        else:
            self.mainmenu.display(self.screen)
            self.mainmenu.update(self.event)

        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        while True:
            self.update()
