import pygame, random
from src.UI.background import Background
from .sprites.player import Player
from .sprites.enemy import ShooterEnemy, SelfKillerEnemy
from .settings import WIDTH, HEIGHT, G_SPRITE_SIZE, ShipTypes


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.background = Background()

        self.visible_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_bullet_group = pygame.sprite.Group()
        self.player_bullet_group = pygame.sprite.Group()

        self.max_enemy_count = 15

        self.player = Player(
            (WIDTH // 2 - G_SPRITE_SIZE // 2, HEIGHT - G_SPRITE_SIZE),
            visible_group=self.visible_group,
            bullet_group=self.player_bullet_group,
        )

    def spawn_enemy(self):
        if random.uniform(0, 1) < 0.01:
            random_x = random.randint(-WIDTH, WIDTH * 2)
            random_y = random.randint(-HEIGHT, 0)
            SelfKillerEnemy((random_x, random_y), self.visible_group, [])

        if len(self.enemy_group) >= self.max_enemy_count:
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

    def handle_player_attack(self):
        for bullet in self.player_bullet_group.sprites():
            collided_enemy = pygame.sprite.spritecollideany(bullet, self.enemy_group)
            if collided_enemy is not None and pygame.sprite.collide_mask(
                bullet, collided_enemy
            ):
                bullet.kill()
                collided_enemy.kill()
                break

    def run(self):
        self.background.update()
        self.visible_group.update(relative_rect=self.player.rect)
        self.background.draw_background(self.display_surface)
        self.visible_group.draw(self.display_surface)

        self.spawn_enemy()
        self.handle_player_attack()
