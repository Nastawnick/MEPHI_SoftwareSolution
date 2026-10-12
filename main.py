import pygame
from config import WIDTH, HEIGHT
from game import Game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космический тир")
clock = pygame.time.Clock()
game = Game()

running = True
while running:
    clock.tick(game.fps_limit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            game.on_key(event.key)

    game.update(dt=min(clock.tick(game.fps_limit) / 1000, 0.05), keys=pygame.key.get_pressed())
    game.draw(screen, clock.get_fps())
    pygame.display.flip()

pygame.quit()
