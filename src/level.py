from typing import Optional
import pygame, random
from src.storage.storage import Storage
from src.soundmanager.soundmanager import Soundmanager
from src.UI.background import Background
from src.UI.healthbar import Healthbar
from src.animation.Text.colortransition import ColorTransition
from src.timer.cooldown import Cooldown
from src.powerops.powerops import Powerops
from .sprites.ships.player import Player
from .sprites.ships.enemy import ShooterEnemy, SelfKillerEnemy
from .sprites.obstacles.asteroid import Asteroid
from .settings import WIDTH, HEIGHT, G_SPRITE_SIZE, ShipTypes
from config import FONT_DIR


class Level:
    def __init__(self, level: int):
        self.display_surface = pygame.display.get_surface()

        title_font = pygame.font.Font(FONT_DIR / "BarcadeNoBarBold-gzXq.otf", 100)
        self.title_blit_cooldown = Cooldown(4000)
        self.level_title = ColorTransition(
            text=f"level {level}",
            size=100,
            font=title_font,
            factor=10,
            change_color=False,
        )

        self.is_gameover = False

        self.background = Background()
        self.health_bar = Healthbar(Storage.get_player_data().get("health_count"))

        self.visible_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.player_bullet_group = pygame.sprite.Group()
        self.powerops_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()

        self.level_attributes = Storage.get_level_data(level)

        self.current_level = level
        self.enemy_count = 0

        range_ = self.level_attributes.get("max_spawn_count")
        self.powerops_index = [
            random.randint(0, range_) for _ in range((level // 3) + 1)
        ]
        self.p_opsed_enemies = []

        self.player = Player(
            (WIDTH // 2 - G_SPRITE_SIZE // 2, HEIGHT - G_SPRITE_SIZE),
            visible_group=self.visible_group,
            bullet_group=self.player_bullet_group,
        )

        """this is temporary solution, I have zero idea how
           a single bullet is always present in player bullet group"""
        self.player_bullet_group.empty()

        Soundmanager.play_main_channel()

    def display_title(self):
        self.title_blit_cooldown.handle_cooldown()
        if not self.title_blit_cooldown.has_cooldown():
            self.level_title.display((WIDTH, HEIGHT), self.display_surface)

    def start_title_display_cooldown(self):
        self.title_blit_cooldown.reset_time()

    def completed(self):
        return (
            self.enemy_count >= self.level_attributes.get("max_spawn_count")
            and len(self.enemy_group.sprites()) == 0
        )

    def spawn_enemy(self):
        if len(self.enemy_group.sprites()) >= self.level_attributes.get(
            "spawn_count"
        ) or self.enemy_count >= self.level_attributes.get("max_spawn_count"):
            return

        shooter_probability = self.level_attributes["enemies"]["shooter"]
        self_killer_probability = self.level_attributes["enemies"]["self_killer"]
        enemy_choice = random.choices(
            ("shooter", "self_killer"),
            (shooter_probability, self_killer_probability),
            k=1,
        )

        if enemy_choice[0] == "self_killer":
            random_x = random.randint(0, WIDTH)
            random_y = random.randint(-HEIGHT, 0)
            SelfKillerEnemy(
                (random_x, random_y),
                visible_group=self.visible_group,
                base_group=self.enemy_group,
            )
        else:
            do_collide = False
            random_x = random.randint(-WIDTH, WIDTH * 2)
            random_y = random.randint(-HEIGHT, 0)
            for sprite in self.enemy_group.sprites():
                checker_rect = pygame.Rect(
                    random_x, sprite.rect.y, G_SPRITE_SIZE, G_SPRITE_SIZE
                )
                if sprite.rect.colliderect(checker_rect):
                    do_collide = True
                    break

            if not do_collide:
                ShooterEnemy(
                    pos=(random_x, random_y),
                    visible_group=self.visible_group,
                    base_group=self.enemy_group,
                    bullet_group=self.enemy_bullet_group,
                    offset_y=random.randrange(0, G_SPRITE_SIZE * 4),
                )
                self.enemy_count += 1

    def spawn_obstacle(self):
        if random.uniform(0, 1) < 0.01:
            random_x = random.randint(0, WIDTH)
            random_y = random.randint(-HEIGHT * 2, 0 - G_SPRITE_SIZE)
            Asteroid((random_x, random_y), self.visible_group, self.obstacle_group)

    def spawn_powerops(self):
        if self.enemy_count in self.powerops_index:
            self.powerops_index.remove(self.enemy_count)
            current_enemy_group_len = len(self.enemy_group.sprites())
            enemy_index = (
                int(self.enemy_count / self.level_attributes.get("max_spawn_count"))
                * current_enemy_group_len
            ) % current_enemy_group_len
            self.p_opsed_enemies.append(self.enemy_group.sprites()[enemy_index])
            self.enemy_group.sprites()[enemy_index].image.fill("red")
            print(self.p_opsed_enemies, self.powerops_index)
        "copy each time because me are removing from currently iterating array"
        for sprite in self.p_opsed_enemies[:]:
            if not sprite.alive():
                power_type = random.choice(["missile"])
                action_group = {
                    "laser": self.player_bullet_group,
                    "missile": self.player_bullet_group,
                }
                Powerops(
                    power_type,
                    base_group=self.powerops_group,
                    visible_group=self.visible_group,
                    action_group=action_group.get(power_type, None),
                )
                self.p_opsed_enemies.remove(sprite)

    def handle_player_attack(self):
        for bullet in self.player_bullet_group.sprites():
            collided_enemy = pygame.sprite.spritecollideany(bullet, self.enemy_group)
            if get_instance_cls(bullet) == "Laser":
                if collided_enemy is not None and bullet.rect.colliderect(
                    collided_enemy
                ):
                    collided_enemy.damage(bullet.get_damage())
                    bullet.handle_kill()
            elif collided_enemy is not None and pygame.sprite.collide_mask(
                bullet, collided_enemy
            ):
                collided_enemy.damage(bullet.get_damage())
                bullet.handle_kill()

        for bullet in self.player_bullet_group.sprites():
            for obstacle in self.obstacle_group.sprites():
                if (
                    not obstacle.is_active()
                    and obstacle.rect.colliderect(bullet.rect)
                    and pygame.sprite.collide_mask(bullet, obstacle)
                ):
                    obstacle.active()
                    bullet.handle_kill()

    def handle_enemy_attack(self):
        for bullet in self.enemy_bullet_group.sprites():
            player_bullet_collision = pygame.sprite.collide_rect(bullet, self.player)
            if player_bullet_collision and pygame.sprite.collide_mask(
                bullet, self.player
            ):
                bullet.kill()
                self.reduce_player_health(bullet.get_damage())

        for enemy in self.enemy_group.sprites():
            if enemy.rect.colliderect(self.player.rect):
                self.reduce_player_health(1)

    def handle_obstacle_collision(self):
        for obstacle in self.obstacle_group.sprites():
            if obstacle.rect.colliderect(
                self.player.rect
            ) and pygame.sprite.collide_mask(self.player, obstacle):
                obstacle.active()
                self.reduce_player_health(1)

    def reduce_player_health(self, damage: int):
        self.player.damage(damage)

    def handle_gameover(self):
        if self.player.is_dead() and self.player.can_kill():
            self.is_gameover = True

    def run(self, event: Optional[pygame.event.Event]):
        self.background.update()
        self.health_bar.update(self.player.get_damage_count())
        self.visible_group.update(player=self.player)

        self.background.draw_background(self.display_surface)
        self.visible_group.draw(self.display_surface)
        self.health_bar.display(self.display_surface)

        self.display_title()

        self.spawn_enemy()
        self.spawn_obstacle()
        self.spawn_powerops()
        self.handle_player_attack()
        self.handle_enemy_attack()
        self.handle_obstacle_collision()
        self.handle_gameover()


def get_instance_cls(instance: object):
    return instance.__class__.__name__
