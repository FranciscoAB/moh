import pygame
from Util import *
from random import randint

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.health = 1
        self.scoreValue = 1

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

    def damage(self, damage):
        self.health -= damage

    

class EnemyBig(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        
        self.image = pygame.image.load("enemyBig.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.health = 3
        self.scoreValue = 2

        self.updateTimerLimit = 2
        self.updateTimer = 0
        
class EnemySpaceship(Enemy):
    def __init__(self):
        Enemy.__init__(self)

        self.image = pygame.image.load("enemySpaceship.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        self.scoreValue = 5

        self.updateTimerLimit = 3

        self.direction = randint(0, 1)

        self.rect.x = 0
        self.rect.y = randint(0, DISPLAY_HEIGHT_GAMEZONE / 6)
        
        if self.direction == 0:
            self.direction = -1
            self.rect.x = DISPLAY_WIDTH_GAMEZONE - self.rect.w
        
    def update(self, deltaTime):
        if self.updateTimer >= self.updateTimerLimit:
            self.rect.x += self.direction
            self.updateTimer = 0
        self.updateTimer += deltaTime

    def mustDie(self):
        if self.rect.x > DISPLAY_HEIGHT_GAMEZONE or self.rect.x < 0:
            return True
        else:
            return False
