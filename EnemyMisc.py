import pygame
from Util import *
from random import randint

class Enemy():
    def __init__(self):
        self.health = 0
        self.updateTimerLimit = 0
        self.updateTimer = 0

    def damage(self, damage):
        self.health -= damage

class EnemyNormal(pygame.sprite.Sprite, Enemy):
    def __init__(self):
        Enemy.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("enemy.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.initialHealth = 1
        self.health = 1
        self.scoreValue = 1

    def update(self, dt):
        self.updateTimer += dt

        if self.updateTimer >= self.updateTimerLimit:
            self.rect.y += 1
            self.updateTimer = 0
        
        if self.rect.y > DISPLAY_HEIGHT_GAMEZONE:
            self.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - self.rect.w)
            self.rect.y = 0
            self.updateTimerLimit = randint(2, 10)
            self.health = self.initialHealth
            

class EnemyBig(pygame.sprite.Sprite, Enemy):
    def __init__(self):
        Enemy.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("enemyBig.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.initialHealth = 3
        self.health = 3
        self.scoreValue = 2

    def update(self, dt):
        self.updateTimer += dt

        if self.updateTimer >= self.updateTimerLimit:
            self.rect.y += 1
            self.updateTimer = 0
        
        if self.rect.y > DISPLAY_HEIGHT_GAMEZONE:
            self.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - self.rect.w)
            self.rect.y = 0
            self.updateTimerLimit = randint(2, 10)
            self.health = self.initialHealth
        
class EnemySpaceship(pygame.sprite.Sprite, Enemy):
    def __init__(self):
        Enemy.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("enemySpaceship.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        self.scoreValue = 10

        self.updateTimerLimit = 2
        self.updateTimer = 0

        self.direction = randint(0, 1)

        self.rect.x = 0
        self.rect.y = randint(0, DISPLAY_HEIGHT_GAMEZONE / 6)
        
        if self.direction == 0:
            self.direction = -1
            self.rect.x = DISPLAY_WIDTH_GAMEZONE - self.rect.w
        
    def update(self, dt):
        self.updateTimer += dt

        if self.updateTimer >= self.updateTimerLimit:
            self.rect.x += self.direction
            self.updateTimer = 0

    def mustDie(self):
        if self.rect.x > DISPLAY_HEIGHT_GAMEZONE or self.rect.x < 0:
            return True
        else:
            return False