import pygame, sys, time
from src.storage.storage import Storage
from src.level import Level
from src.notification.manager import NotificationManager
from src.UI.shop.shop import ShopManager
from src.UI.menu.mainmenu import MainMenuUI
from src.UI.menu.gameover import GameoverUI
from src.animation.Text.fadeout import Fadeout
from src.settings import FPS, WIDTH, HEIGHT
from src.constants import BLACK


class Manager:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.quit_game = False
        self.start_game = False
        self.event = None

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.level = Level(level=Storage.get_current_level())

        self.notification_manager = NotificationManager()
        self.shop = ShopManager((WIDTH, HEIGHT))

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

        # if player return to main menu by quitting current game
        self.is_level_quited = False

    def handle_event(self):
        self.event = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True
                Storage.write_current_level(
                    max(Storage.get_current_level(), self.level.current_level)
                )
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                or event.type == pygame.MOUSEBUTTONUP
                or event.type == pygame.MOUSEWHEEL
            ):
                self.event = event
            if not self.start_game:
                self.shop.process_events(event)
                self.shop.handle_events(event, self.notification_manager)

        if self.quit_game:
            Storage.write_current_level(
                max(Storage.get_current_level(), self.level.current_level)
            )
            sys.exit()

    def replay(self):
        prev_background = self.level.background.get_surfaces()
        self.level.is_gameover = False
        self.level = Level(self.level.current_level)
        self.level.background.load_surfaces(prev_background)
        self.level.start_title_display_cooldown()

    def end_game(self):
        self.quit_game = True

    def play(self):
        self.start_game = True
        self.level.start_title_display_cooldown()

    def return_menu(self):
        self.load_level(self.level.current_level, False)
        self.level.is_gameover = False
        self.start_game = False

    def load_level(self, level: int, auto_start: bool = True):
        self.level = Level(level)
        if auto_start:
            self.play()

    def update(self):
        time_delta = self.clock.tick(FPS) / 1000.0
        self.handle_event()

        if self.start_game:
            self.level.run(self.event)
            if self.level.is_gameover:
                self.gameover.display(self.screen)
                self.gameover.update(self.event)
                self.mainmenu.update_levels(self.level.current_level)
            elif self.level.completed():
                Storage.write_reward_point(self.level.current_level)
                Storage.write_current_level(self.level.current_level + 1)
                Storage.write_player_data(self.level.get_player_coin())
                self.load_level(self.level.current_level + 1)
        elif not self.shop.isopen():
            self.mainmenu.display(self.screen)
            self.mainmenu.update(self.event)
        if not self.start_game:
            self.shop.update(time_delta)
            self.shop.draw_ui(self.screen)

        self.notification_manager.manage()
        self.notification_manager.draw(self.screen)

        pygame.display.update()

    def run(self):
        while True:
            self.update()
