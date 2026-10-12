import random
import pygame
from config import WIDTH, HEIGHT, BACKGROUND, TEXT
from entities import Player, Bullet
from enemy import Enemy


class Game:
    def __init__(self):
        self.player = Player()
        self.bullets = []
        self.enemies = [Enemy() for _ in range(8)]
        self.stars = [(random.randrange(WIDTH), random.randrange(HEIGHT)) for _ in range(80)]
        self.font = pygame.font.SysFont("arial", 16)
        self.score = 0
        self.checks = 0
        self.debug = False
        self.fps_limit = 60

    def on_key(self, key):
        if key == pygame.K_F1:
            self.debug = not self.debug
        if key == pygame.K_l:
            self.fps_limit = 20 if self.fps_limit == 60 else 60
        if key == pygame.K_EQUALS:
            self.enemies += [Enemy() for _ in range(50)]

    def update(self, dt, keys):
        self.player.update(dt, keys)
        if keys[pygame.K_SPACE] and self.player.can_shoot():
            self.bullets.append(Bullet(self.player.x, self.player.y - 20))

        for bullet in self.bullets:
            bullet.update(dt)
        self.bullets = [b for b in self.bullets if b.y > 0]
        for enemy in self.enemies:
            enemy.update(dt, self.player)

        self.check_collisions()

    def check_collisions(self):
        self.checks = 0
        for bullet in self.bullets[:]:
            for enemy in self.enemies:
                self.checks += 1
                if collide(bullet, enemy):
                    self.bullets.remove(bullet)
                    self.on_hit(enemy)
                    break

    def on_hit(self, enemy):
        enemy.hit()
        if enemy.hp == 0:
            self.score += 1
            enemy.respawn()

    def draw(self, screen, fps):
        screen.fill(BACKGROUND)
        for star in self.stars:
            screen.set_at(star, (120, 130, 150))

        for obj in self.enemies + self.bullets:
            obj.draw(screen)
        self.player.draw(screen)

        if self.debug:
            for enemy in self.enemies:
                label = self.font.render(enemy.state, True, enemy.color())
                screen.blit(label, (enemy.x - label.get_width() / 2, enemy.y - 34))
        self.draw_hud(screen, fps)

    def draw_hud(self, screen, fps):
        lines = [
            f"FPS: {fps:.0f} (лимит {self.fps_limit}, клавиша L)",
            f"Создано пуль: {Bullet.created}",
            f"Врагов: {len(self.enemies)} (клавиша = добавляет 50)",
            f"Проверок столкновений: {self.checks}",
            f"Счёт: {self.score}",
        ]
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, 380, 112))
        for i, line in enumerate(lines):
            screen.blit(self.font.render(line, True, TEXT), (10, 10 + i * 20))


def collide(a, b):
    distance = a.RADIUS + b.RADIUS
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2 < distance ** 2
