import pygame
import sys
import time
from src.storage.storage import Storage
from src.level import Level
from src.soundmanager.soundmanager import Soundmanager
from src.notification.manager import NotificationManager
from src.UI.shop.shop import ShopManager
from src.UI.menu.mainmenu import MainMenuUI
from src.UI.menu.gameover import GameoverUI
from src.UI.menu.pausemenu import PauseMenu  # Import the PauseMenu class
from src.settings import FPS, WIDTH, HEIGHT
from src.constants import BLACK


class Manager:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.quit_game = False
        self.start_game = False
        self.game_paused = False
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
        self.mainmenu = MainMenuUI(
            (WIDTH // 2, HEIGHT // 2),
            {
                "play": lambda: self.play(),
                "load_level": lambda level: self.load_level(level),
                "exit": lambda: self.end_game(),
            },
        )

        self.pausemenu = PauseMenu(
            (WIDTH // 2, HEIGHT // 2),
            {
                "resume": lambda: self.resume_game(),
                "restart": lambda: self.replay(),
                "quit": lambda: self.return_menu(),
            },
        )

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_paused = not self.game_paused
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
        self.game_paused = False
        self.level = Level(self.level.current_level)
        self.level.background.load_surfaces(prev_background)
        self.level.start_title_display_cooldown()

    def end_game(self):
        self.quit_game = True

    def play(self):
        self.start_game = True
        self.level.start_title_display_cooldown()

    def resume_game(self):
        self.game_paused = False

    def return_menu(self):
        self.load_level(self.level.current_level, False)
        self.level.is_gameover = False
        self.start_game = False
        self.game_paused = False

    def load_level(self, level: int, auto_start: bool = True):
        self.level = Level(level)
        if auto_start:
            self.play()

    def update(self):
        time_delta = self.clock.tick(FPS) / 1000.0
        self.handle_event()

        if self.start_game and not self.game_paused:
            self.level.run(self.event)
            if self.level.is_gameover:
                self.gameover.display(self.screen)
                self.gameover.update(self.event)
                self.mainmenu.update_levels(self.level.current_level)
            elif self.level.completed():
                Soundmanager.stop_sfx_channels()
                Storage.write_reward_point(self.level.current_level)
                Storage.write_current_level(self.level.current_level + 1)
                Storage.write_player_data(self.level.get_player_coin())
                self.load_level(self.level.current_level + 1)
        elif not self.shop.isopen() and not self.game_paused:
            self.mainmenu.display(self.screen)
            self.mainmenu.update(self.event)
        if not self.start_game:
            self.shop.update(time_delta)
            self.shop.draw_ui(self.screen)

        if self.start_game and self.game_paused:
            self.pausemenu.display(self.screen)
            self.pausemenu.update(self.event)

        self.notification_manager.manage()
        self.notification_manager.draw(self.screen)

        pygame.display.update()

    def run(self):
        while True:
            self.update()
