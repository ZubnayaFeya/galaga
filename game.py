import pygame
import sys

import pyganim

from constats import *
from game_obj import Player, Background, Plasmoid, Meteorite

pygame.init()
pygame.display.set_caption(TITLE)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HIGTH))
clock = pygame.time.Clock()

explostion_animation = pyganim.PygAnimation(
    [('assets/blue_explosion/1_%s.png' % i, 50) for i in range(17)],
    loop=False)

# music = pygame.mixer.Sound('assets/music/game.wav')
# music.play(-1)

all_obj = pygame.sprite.Group()
plasmoids = pygame.sprite.Group()
meteors = pygame.sprite.Group()

explosions = []

player = Player(clock, plasmoids)
background = Background()

all_obj.add(background, player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # pygame.quit('0')
            # break
            sys.exit('0')

    # screen.fill(BLACK)

    # player.update()
    # background.update()

    Meteorite.process_metore(clock, meteors)

    all_obj.update()
    plasmoids.update()
    meteors.update()

    for collided in pygame.sprite.groupcollide(plasmoids, meteors, True, True):
        explosion = explostion_animation.getCopy()
        explosion.play()
        explosions.append((explosion, (collided.rect.center)))

    if pygame.sprite.spritecollide(player, meteors, False):  # todo заменить на тру
        all_obj.remove(player)  # todo почему то песонаж остался на месте хоть и не отрисован


    # screen.blit(background.image, background.rect)
    # screen.blit(player.image, player.rect)
    all_obj.draw(screen)
    plasmoids.draw(screen)
    meteors.draw(screen)

    for explosion, position in explosions.copy():
        if explosion.isFinished():
            explosions.remove((explosion, position))
        else:
            x, y = position
            explosion.blit(screen, (x - 128, y - 128))

    pygame.display.flip()
    clock.tick(FPS)

