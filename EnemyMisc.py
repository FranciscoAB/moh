import pygame
from Util import *
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.updateTimerLimit = 2
        self.updateTimer = 0

    def update(self, deltaTime):
        if self.updateTimer >= self.updateTimerLimit:
            self.rect.y += 1
            self.updateTimer = 0
        self.updateTimer += deltaTime
        
        if self.rect.y > DISPLAY_HEIGHT_GAMEZONE:
            self.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - self.rect.w)
            self.rect.y = 0
            self.updateTimerLimit = randint(2, 10)
