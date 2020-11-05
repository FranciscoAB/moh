import pygame
from Util import *
from random import randint

from Animation import *
from SpritesData import *

class Enemy():
    def __init__(self):

        self.tag = "enemy"

        self.health = 1
        self.formationTimerLimitX = 0
        self.formationTimerX = 0
        self.formationTimerLimitY = 0
        self.formationTimerY = 0

        self.followFormationLimit = 1
        self.followFormationTimer = 0

        self.attackTimerLimitX = 0
        self.attackTimerLimitY = 0
        self.attackTimerX = 0
        self.attackTimerY = 0

        self.attackTimerLimitMin = 3000
        self.attackTimerLimitMax = 12000
        self.attackTimerLimit = randint(self.attackTimerLimitMin, self.attackTimerLimitMax)
        self.attackTimer = 0

        self.playerRect = pygame.sprite.Rect(0, 0, 0, 0)

    def damage(self, damage):
        self.health -= damage
        
        if self.health <= 0:
            self.kill()

class EnemyNormal(pygame.sprite.Sprite, Enemy):
    def __init__(self, playerRect):
        Enemy.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.anim = Animation(SP_enemy_normal, pygame.sprite.Rect(0, 0, 0, 0), 400, -1)
        self.rect = self.anim.getCurrentSprite().rect

        #Position which enemy will try to reach
        self.targetPosition = pygame.sprite.Rect(0, 0, 0, 0)

        #If not in formation, it will try to reach the target position
        self.reachedFormation = False
        self.attacking = False

        self.attackTimerLimitX = 10
        self.attackTimerLimitY = 3

        self.speedX = 1
        self.speedY = 1

        self.speedFormationX = 1
        self.speedFormationY = 1

        self.initialHealth = 1
        self.health = 1
        self.scoreValue = 1

        self.playerRect = playerRect
        self.attackingTargetPosition = pygame.sprite.Rect(0, 0, 0, 0)

        #
        self.formationMovementLimit = 5
        self.formationMovementTimer = 0
        self.direction = 0

        #Enemy shots
        self.shotTimerLimit = randint(300, 700)
        self.shotTimer = 0
        self.alreadyShot = False

    def update(self, dt, enemyBulletsList):

        if (not self.reachedFormation) and (not self.attacking):
            self.__goToFormation(dt)

        if (not self.attacking) and (self.reachedFormation):
            self.__followFormation(dt)

        if (self.attacking):
            self.__attack(dt)

        if ((not self.reachedFormation) and (not self.attacking)) or (self.attacking):
            if not (self.alreadyShot):
                if (self.rect.x > 0) and (self.rect.x < DISPLAY_WIDTH_GAMEZONE - self.rect.w):
                    self.shotTimer += dt
                    if (self.shotTimer >= self.shotTimerLimit):
                        enemyBulletsList.add(self.__shot())
                        self.alreadyShot = True
                        self.shotTimer = 0

        if (self.rect.x == self.targetPosition.x) and (self.rect.y == self.targetPosition.y):
            self.reachedFormation = True
            self.alreadyShot = False

        if self.reachedFormation:
            self.attackTimer += dt

            if (self.attackTimer >= self.attackTimerLimit):
                self.speedX = 1
                self.speedY = 1
                self.attacking = True
                self.reachedFormation = False
                self.attackingTargetPosition.x = randint(0, DISPLAY_WIDTH_GAMEZONE - self.anim.getCurrentSprite().rect.w)
                self.attackTimer = 0

        if (self.rect.y > DISPLAY_HEIGHT_GAMEZONE):
            self.attacking = False
            self.reachedFormation = False
            self.rect.y = -self.anim.getCurrentSprite().rect.h
            self.attackTimer = 0
            self.calculateFormationLimits()
            self.attackTimerLimit = randint(self.attackTimerLimitMin, self.attackTimerLimitMax)

        self.anim.update(dt)
        self.image = self.anim.getCurrentSprite().image

    def __goToFormation(self, dt):

        self.formationTimerX += dt
        self.formationTimerY += dt
        
        if self.formationTimerX >= self.formationTimerLimitX:
            if (self.rect.x < self.targetPosition.x):
                self.rect.x += self.speedFormationX
            else:
                self.rect.x -= self.speedFormationX
            self.formationTimerX = 0

        if self.formationTimerY >= self.formationTimerLimitY:
            if (self.rect.y != self.targetPosition.y):
                self.rect.y += self.speedY
            self.formationTimerY = 0
    
    def __followFormation(self, dt):
        self.followFormationTimer += dt
        
        if self.followFormationTimer >= self.followFormationLimit:
            if (self.rect.x < self.targetPosition.x):
                self.rect.x += self.speedFormationX
            else:
                self.rect.x -= self.speedFormationX
            self.followFormationTimer = 0

    def __attack(self, dt):
        self.attackTimerX += dt
        self.attackTimerY += dt

        if self.attackTimerY >= self.attackTimerLimitY:
            self.rect.y += self.speedY
            self.attackTimerY = 0

        if self.attackTimerX >= self.attackTimerLimitX:

            if (self.rect.x > self.attackingTargetPosition.x):
                self.rect.x -= self.speedX
            elif (self.rect.x < self.attackingTargetPosition.x):
                self.rect.x += self.speedX
            self.attackTimerX = 0

    def __shot(self):
        eb = EnemyBullet()
        eb.rect.x = self.rect.x + (self.rect.w / 2) - (eb.rect.w / 2)
        eb.rect.y = self.rect.y + self.rect.h

        return eb

    def calculateFormationLimits(self):

        self.formationTimerX = 0
        self.formationTimerY = 0

        deltaX = self.rect.x - self.targetPosition.x
        deltaY = self.rect.y - self.targetPosition.y

        if (abs(deltaX) >= abs(deltaY)):
            self.formationTimerLimitX = 1

            if (deltaY != 0):
                self.formationTimerLimitY = int(round(abs(deltaX) / abs(deltaY)))
            else:
                self.speedY = 0
        else:
            self.formationTimerLimitY = 1
                
            if (deltaX != 0):
                self.formationTimerLimitX = int(round(abs(deltaY) / abs(deltaX)))
            else:
                self.speedX = 0

        if (deltaX > 0):
            self.speedX *= -1

        if (deltaY > 0):
            self.speedY *= -1

        self.formationTimerLimitX *= 3
        if (self.formationTimerLimitX > FORMATION_LIMIT_TIMER):
            self.formationTimerLimitX = FORMATION_LIMIT_TIMER

        self.formationTimerLimitY *= 3

class EnemyBullet(pygame.sprite.Sprite, Enemy):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Sprites/enemy_bullet.png").convert()
        self.rect = self.image.get_rect()

        self.power = 1

        self.updateTimerLimit = 2
        self.updateTimer = 0

    def update(self, dt):

        self.updateTimer += dt

        if self.updateTimer >= self.updateTimerLimit:
            self.rect.y += 1
            self.updateTimer = 0

        if self.rect.y >= DISPLAY_HEIGHT_GAMEZONE:
            self.kill()