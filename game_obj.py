import random

import pygame

from constats import *


class Plasmoid(pygame.sprite.Sprite):
    speed = -15

    def __init__(self, position):
        super().__init__()

        self.image = pygame.image.load('assets/plasmoid.png')
        self.rect = self.image.get_rect()

        self.rect.midbottom = position

    def update(self):
        self.rect.move_ip((0, self.speed))


class Player(pygame.sprite.Sprite):
    max_speed = 10
    shooting_cooldown = 150

    def __init__(self, clock, plasmoids):
        super().__init__()

        self.clock = clock
        self.plasmoids = plasmoids

        self.image = pygame.image.load('assets/player.png')
        self.rect = self.image.get_rect()

        self.rect.centerx = WINDOW_WIDTH / 2
        self.rect.bottom = WINDOW_HIGTH - 10

        self.current_speed = 0
        self.current_shotting_cooldown = 0

        self.plasmoid_sound = pygame.mixer.Sound('assets/sounds/plasma_bolt.wav')

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.rect.left <= 0:
                self.current_speed = 0
            else:
                self.current_speed = - self.max_speed
        elif keys[pygame.K_RIGHT]:
            if self.rect.right >= WINDOW_WIDTH:
                self.current_speed = 0
            else:
                self.current_speed = self.max_speed
        else:
            self.current_speed = 0

        self.rect.move_ip((self.current_speed, 0))

        self.shootings()

    def shootings(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.current_shotting_cooldown <= 0:
            self.plasmoid_sound.play()
            self.plasmoids.add(Plasmoid(self.rect.midtop))
            self.current_shotting_cooldown = self.shooting_cooldown
        else:
            self.current_shotting_cooldown -= self.clock.get_time()

        for plasmoid in list(self.plasmoids):
            if plasmoid.rect.bottom < 0:
                self.plasmoids.remove(plasmoid)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('assets/background.png')
        self.rect = self.image.get_rect()

        self.rect.bottom = WINDOW_HIGTH

    def update(self):
        self.rect.bottom += 5

        if self.rect.bottom >= self.rect.height:
            self.rect.bottom = WINDOW_HIGTH


class Meteorite(pygame.sprite.Sprite):
    cooldown = 450
    current_cooldown = 0
    speed = 5

    def __init__(self):
        super().__init__()

        image_name = 'assets/meteor%d.png' % random.randint(3, 8)
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()

        self.rect.midbottom = (random.randint(0, WINDOW_WIDTH), 0)

    def update(self):
        self.rect.move_ip((0, self.speed))

    @staticmethod
    def process_metore(clock, meteorites):
        if Meteorite.current_cooldown <= 0:
            meteorites.add(Meteorite())
            Meteorite.current_cooldown = Meteorite.cooldown
        else:
            Meteorite.current_cooldown -= clock.get_time()

        for m in list(meteorites):
            if m.rect.right < 0 or m.rect.left > WINDOW_WIDTH or m.rect.top > WINDOW_HIGTH:
                meteorites.remove(m)
