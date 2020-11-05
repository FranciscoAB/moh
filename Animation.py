import pygame
from Util import *

class Animation():
    def __init__(self, imagesURLs, position, timerLimit, repeatTimes = 0):

        self.timer = 0
        self.timerLimit = timerLimit

        self.sprites = []

        self.spriteIndex = 0

        #If repeatTimes is set to -1, then it will repeat forever
        self.repeatTimes = repeatTimes
        self.repeat = 0

        self.shouldDie = False

        for x in imagesURLs:
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load(x).convert_alpha()
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = position.x
            sprite.rect.y = position.y
            self.sprites.append(sprite)
            sprite = ()

    def update(self, dt):
        
        self.timer += dt

        if self.timer >= self.timerLimit:
            if not (self.spriteIndex >= len(self.sprites) - 1):
                self.spriteIndex += 1
            else:
                if self.repeatTimes == -1:
                    self.spriteIndex = 0
                else:
                    if (self.repeat >= self.repeatTimes):
                        self.shouldDie = True
                    else:
                        self.spriteIndex = 0
                        self.repeat += 1
                
            self.timer = 0

    def getCurrentSprite(self):
        return self.sprites[self.spriteIndex]