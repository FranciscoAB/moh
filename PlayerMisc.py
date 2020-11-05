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

        self.image = pygame.image.load("Sprites/player.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.updateTimerLimit = 3
        self.updateTimer = 0

        self.maxCurrentBullets = 2
        
    '''
    Player Movement functions
    '''
    def move(self, keys, dt):

        self.updateTimer += dt

        if (self.updateTimer >= self.updateTimerLimit):
            if keys[pygame.K_LEFT]:
                self.moveLeft()
            if keys[pygame.K_RIGHT]:
                self.moveRight()
            if keys[pygame.K_UP]:
                self.moveUp()
            if keys[pygame.K_DOWN]:
                self.moveDown()    
            self.updateTimer = 0

    def moveUp(self):
        if self.rect.y > 0:
            self.rect.y -= 2
            
    def moveDown(self):  
        if self.rect.y < DISPLAY_HEIGHT_GAMEZONE - self.rect.height:
            self.rect.y += 2
            
    def moveRight(self):
        if self.rect.x < DISPLAY_WIDTH_GAMEZONE - self.rect.width:
            self.rect.x += 2
        
    def moveLeft(self):
        if self.rect.x > 0:
            self.rect.x -= 2           

'''
Class representing the player bullets.
'''
class PlayerBullet (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Sprites/bullet.png").convert()
        self.rect = self.image.get_rect()

        self.power = 1

        self.updateTimerLimit = 1
        self.updateTimer = 0

    def update(self, dt):

        self.updateTimer += dt

        if self.updateTimer >= self.updateTimerLimit:
            self.rect.y -= 1
            self.updateTimer = 0

        if self.rect.y <= 0:
            self.kill()