import pygame
from random import randint
from Util import *

class Star:
    def __init__(self, win):
        
        self.rect = pygame.draw.rect(win, (1, 1, 1), (0, 0, 0, 0))

        self.rect.w = 5
        self.rect.h = 5

        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

        self.timerBeforeMoveLimit = randint(1, 10)
        self.timerBeforeMove = 0

    def update(self):

        self.timerBeforeMove += 1
        
        if self.timerBeforeMove >= self.timerBeforeMoveLimit:
            self.timerBeforeMove = 0
            self.rect.y += 1

        if self.rect.y > DISPLAY_HEIGHT_GAMEZONE:
            self.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE)
            self.rect.y = 0
            self.speed = randint(1, 2)
            self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
        
        
