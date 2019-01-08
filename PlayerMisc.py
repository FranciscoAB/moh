import pygame
from Util import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
    def moveUp(self):
        if self.rect.y > 0:
            self.rect.y -= 1        
    def moveDown(self):
        if self.rect.y < DISPLAY_HEIGHT - self.rect.height:
            self.rect.y += 1
    def moveRight(self):
        if self.rect.x < DISPLAY_WIDTH - self.rect.width:
            self.rect.x += 1
    def moveLeft(self):
        if self.rect.x > 0:
            self.rect.x -= 1
            

class PlayerBullet (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("bullet.png").convert()
        self.rect = self.image.get_rect()
        self.speed_y = 5

    def update(self):
        self.rect.y -= self.speed_y

    def mustDie(self):
        if self.rect.y < 0:
            return True
        else:
            return False