import pygame
from Util import *
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.timerBeforeMoveLimit = randint(1, 2)
        self.timerBeforeMove = 0

    def update(self):
        
        self.timerBeforeMove += 1
        
        if self.timerBeforeMove >= self.timerBeforeMoveLimit:
            self.timerBeforeMove = 0
            self.rect.y += 1            
        
        if self.rect.y > DISPLAY_HEIGHT_GAMEZONE:
            self.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - self.rect.w)
            self.timerBeforeMoveLimit = randint(1, 2)
            self.rect.y = 0
