import pygame
from Util import *

class GameDisplay:
    def __init__(self, win):

        self.rect = pygame.draw.rect(win, (0, 0, 0), (0, 0, 0, 0))

        self.color = (255, 255, 255)

        self.rect.w = DISPLAY_WIDTH_TOTAL - DISPLAY_WIDTH_GAMEZONE
        self.rect.h = DISPLAY_HEIGHT_TOTAL
        self.rect.x = DISPLAY_WIDTH_GAMEZONE
        self.rect.y = 0

