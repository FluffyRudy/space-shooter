import pygame, random
from src.storage.storage import Storage
from src.UI.background import Background
from src.UI.healthbar import Healthbar
from .sprites.ships.player import Player
from .sprites.ships.enemy import ShooterEnemy, SelfKillerEnemy
from .sprites.obstacles.asteroid import Asteroid
from .settings import WIDTH, HEIGHT, G_SPRITE_SIZE, ShipTypes


class Level:
    def __init__(self, level: int):
        self.display_surface = pygame.display.get_surface()

        self.background = Background()
        self.health_bar = Healthbar(5)

        self.visible_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.player_bullet_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()

        self.level_attributes = Storage.get_level_data(level)
        self.current_level = level
        self.enemy_count = 0

        self.player = Player(
            (WIDTH // 2 - G_SPRITE_SIZE // 2, HEIGHT - G_SPRITE_SIZE),
            visible_group=self.visible_group,
            bullet_group=self.player_bullet_group,
        )

        """this is temporary solution, I have zero idea how
           a single bullet is always present in player bullet group"""
        self.player_bullet_group.empty()

    def completed(self):
        return (
            self.enemy_count >= self.level_attributes.get("max_spawn_count")
            and len(self.enemy_group.sprites()) == 0
        )

    def spawn_enemy(self):
        if random.uniform(0, 1) < 0.01:
            random_x = random.randint(-WIDTH, WIDTH * 2)
            random_y = random.randint(-HEIGHT, 0)
            SelfKillerEnemy((random_x, random_y), self.visible_group, self.enemy_group)

        if len(self.enemy_group.sprites()) >= self.level_attributes.get(
            "spawn_count"
        ) or self.enemy_count >= self.level_attributes.get("max_spawn_count"):
            return

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
            random_y = random.randrange(-HEIGHT * 2, HEIGHT * 2, HEIGHT)
            Asteroid((random_x, random_y), self.visible_group, self.obstacle_group)

    def handle_player_attack(self):
        for bullet in self.player_bullet_group.sprites():
            collided_enemy = pygame.sprite.spritecollideany(bullet, self.enemy_group)
            if collided_enemy is not None and pygame.sprite.collide_mask(
                bullet, collided_enemy
            ):
                collided_enemy.damage(bullet.get_damage())
                bullet.kill()
                break

    def handle_enemy_attack(self):
        for bullet in self.enemy_bullet_group.sprites():
            player_bullet_collision = pygame.sprite.collide_rect(bullet, self.player)
            if (
                not self.player.is_invincible
                and player_bullet_collision
                and pygame.sprite.collide_mask(bullet, self.player)
            ):
                self.player.is_invincible = True
                self.player.invincility_cooldown_timer.reset_time()
                bullet.kill()
                self.player.damage(bullet.get_damage())
                self.health_bar.update_health_count(self.player.get_damage_count())
                break

        for enemy in self.enemy_group.sprites():
            if (
                enemy.rect.colliderect(self.player.rect)
                and not self.player.is_invincible
            ):
                self.player.damage(1)
                self.health_bar.update_health_count(self.player.get_damage_count())
                self.player.is_invincible = True
                self.player.invincility_cooldown_timer.reset_time()
                break

    def run(self):
        self.background.update()
        if not self.player.status.is_dead():
            self.visible_group.update(relative_rect=self.player.rect)
        else:
            self.player.update()

        self.background.draw_background(self.display_surface)
        self.visible_group.draw(self.display_surface)
        self.health_bar.display(self.display_surface)

        self.spawn_enemy()
        self.spawn_obstacle()
        self.handle_player_attack()
        self.handle_enemy_attack()
