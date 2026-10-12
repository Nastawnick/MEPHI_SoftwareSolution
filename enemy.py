import random
import pygame
from config import WIDTH, HEIGHT


class Enemy:
    RADIUS = 14

    def __init__(self):
        self.respawn()

    def respawn(self):
        self.x = random.uniform(40, WIDTH - 40)
        self.y = random.uniform(40, 200)
        self.direction = random.choice([-1, 1])
        self.hp = 3
        self.flash = 0         # кадров белой вспышки после попадания
        self.state = "патруль"
        self.SPEED = 120 #пикселей в секунду

    def update(self, dt, player):
        self.flash -= 1
        if self.state == "патруль":
            self.x += self.direction * self.SPEED * dt
            if self.x < 20 or self.x > WIDTH - 20:
                self.direction *= -1
            if abs(player.x - self.x) < 100:
                self.state = "погоня"
        elif self.state == "погоня":
            self.x += (player.x - self.x) * 0.03 * dt
            self.y += self.SPEED // 2 * dt
            if self.y > HEIGHT / 2:
                self.respawn()     # TODO: вместо этого — атака
            if abs(player.x - self.x) > 200:
                self.state = "патруль"

    def hit(self):
        self.hp -= 1
        self.flash = 6

    def color(self):
        if self.flash > 0:
            return (255, 255, 255)
        if self.state == "патруль":
            return (60, 180, 190)
        return (240, 160, 60)

    def draw(self, screen):
        radius = self.RADIUS - (3 - self.hp) * 3   # чем меньше жизней, тем меньше круг
        pygame.draw.circle(screen, self.color(), (self.x, self.y), radius)
