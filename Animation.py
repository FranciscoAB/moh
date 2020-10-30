import pygame
from Util import *

class Animation():
    def __init__(self, imagesURLs, baseRect, timerLimit):

        self.timer = 0
        self.timerLimit = timerLimit

        self.sprites = []

        self.spriteIndex = 0

        self.shouldDie = False

        for x in imagesURLs:
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load(x).convert_alpha()
            sprite.rect = baseRect.rect
            self.sprites.append(sprite)
            sprite = ()

    def update(self, dt):
        
        self.timer += dt

        if self.timer >= self.timerLimit:
            if not (self.spriteIndex >= len(self.sprites) - 1):
                self.spriteIndex += 1
            else:
                self.shouldDie = True
                
            self.timer = 0

    def getCurrentSprite(self):
        return self.sprites[self.spriteIndex]