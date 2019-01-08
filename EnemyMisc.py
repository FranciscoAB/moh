import pygame
from Util import *
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.speed_y = 1

    def update(self):
        if self.rect.y > DISPLAY_HEIGHT:
            self.rect.x = randint(0, DISPLAY_WIDTH)
            self.rect.y = 0
            
        self.rect.y += self.speed_y