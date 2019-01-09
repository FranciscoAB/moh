import pygame
from Util import *

'''
Class representing the player.
'''
class Player(pygame.sprite.Sprite):
    '''
    Constructor
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.updateTimerLimit = 2
        self.updateTimer = 0

        self.maxCurrentBullets = 3
        
    '''
    Player Movement functions
    '''
    def moveUp(self):
        if self.rect.y > 0:
            self.rect.y -= 1
            
    def moveDown(self):  
        if self.rect.y < DISPLAY_HEIGHT_GAMEZONE - self.rect.height:
            self.rect.y += 1
            
    def moveRight(self):
        if self.rect.x < DISPLAY_WIDTH_GAMEZONE - self.rect.width:
            self.rect.x += 1
        
    def moveLeft(self):
        if self.rect.x > 0:
            self.rect.x -= 1            

'''
Class representing the player bullets.
'''
class PlayerBullet (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("bullet.png").convert()
        self.rect = self.image.get_rect()

        self.updateTimerLimit = 1
        self.updateTimer = 0

    def update(self, deltaTime):
        if self.updateTimer >= self.updateTimerLimit:
            self.rect.y -= 1
            self.updateTimer = 0
        self.updateTimer += 1

    def mustDie(self):
        if self.rect.y <= 0:
            return True
        else:
            return False
