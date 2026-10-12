import pygame
from config import WIDTH, HEIGHT, SHIP, BULLET


class Player:
    SPEED = 300          # НЕ пикселей за кадр - Пикселей в секунду
    COOLDOWN = 0.15       # НЕ кадров между выстрелами - Секунд между выстрелами

    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT - 50
        self.reload = 0

    def update(self, dt, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.SPEED * dt
        if keys[pygame.K_RIGHT]:
            self.x += self.SPEED * dt
        self.x = max(20, min(WIDTH - 20, self.x))
        self.reload -= 1 * dt

    def can_shoot(self):
        if self.reload > 0:
            return False
        self.reload = self.COOLDOWN 
        return True

    def draw(self, screen):
        points = [(self.x, self.y - 20), (self.x - 16, self.y + 14), (self.x + 16, self.y + 14)]
        pygame.draw.polygon(screen, SHIP, points)


class Bullet:
    SPEED = 600
    RADIUS = 4
    created = 0        # сколько пуль создано за всю игру

    def __init__(self, x, y):
        self.x, self.y = x, y
        Bullet.created += 1

    def update(self, dt):
        self.y -= self.SPEED * dt

    def draw(self, screen):
        pygame.draw.circle(screen, BULLET, (self.x, self.y), self.RADIUS)

class Pool:
    def __init__(self, create, size):
        self.create = create
        self.items = [create() for _ in range(size)]
    def get(self):
        for item in self.items:
            if not item.active:
                item.active = True
                return item
        item = self.create()
        item.active = True
        self.items.append(item)
        return item
    def active(self):
        return [item for item in self.items if item.active]
    