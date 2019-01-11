import pygame

import time
from random import randint

from PlayerMisc import *
from EnemyMisc import *
from EnvironmentMisc import *
from GameDisplay import *

from Util import *

from Score import *


class Game:

    def __init__(self, win): 
        '''
        Initialization
        '''
        self.win = win
        
        '''
        Player
        '''
        #Group of sprites that represent the player
        self.all_sprites = pygame.sprite.Group()
        
        #Creates and initializes the player
        self.player = Player()
        self.player.rect.x = DISPLAY_WIDTH_GAMEZONE / 2
        self.player.rect.y = DISPLAY_HEIGHT_GAMEZONE - self.player.rect.h
        self.all_sprites.add(self.player)
        
        '''
        Player Bullets
        '''
        #Group of sprites that represent player bullets
        self.playerBulletList = pygame.sprite.Group()
        
        '''
        Enemies
        '''
        #Group of sprites that represent enemies
        self.enemiesList = pygame.sprite.Group()
        
        #Keeps track of enemies amount
        self.enemiesCount = 0
        
        self.timeBeforeGeneration = randint(8000, 30000)
        self.generationTimer = 0
                
        self.enemySpaceship = pygame.sprite.Group()
        
        '''
        Stars
        '''
        self.starsList = []
        
        for x in range(0, STARS_COUNT):
            self.star = Star(self.win)
            self.star.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE)
            self.star.rect.y = randint(0, DISPLAY_HEIGHT_GAMEZONE)
            self.starsList.append(self.star)
        
        '''
        GameDisplay
        '''
        self.gameDisplay = GameDisplay(self.win)
        
        #Score number
        self.score = Score()
        
        #Game display score (text)
        self.myFont = pygame.font.SysFont("Roboto", 50)
        self.scoreText = "Score: 0"
        self.textSurface = self.myFont.render(self.scoreText, False, BLACK)
        
        '''
        Game Loop
        '''
        #Sets the initial state of the main loop
        self.run = True
        
        self.before = pygame.time.get_ticks()
        self.deltaTime = 0
        
        
	#Main loop of the game
    def loop(self):
        while self.run:
            
            self.deltaTime = pygame.time.get_ticks() - self.before
            self.before = pygame.time.get_ticks()
        
            #Checks for user input, to exit from the game
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player.updateTimer = self.player.updateTimerLimit
                        
                if event.type == pygame.KEYDOWN:
                    #Player shot
                    if event.key == pygame.K_SPACE or event.key == pygame.K_LCTRL:
                        if len(self.playerBulletList) < self.player.maxCurrentBullets:
                            self.playerBullet = PlayerBullet()
                            self.playerBullet.rect.x = self.player.rect.x + self.player.rect.width / 2 - self.playerBullet.rect.width / 2
                            self.playerBullet.rect.y = self.player.rect.y - self.playerBullet.rect.height
                            self.playerBulletList.add(self.playerBullet)
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
        
            '''
            mouseState = pygame.mouse.get_pressed()
        
            if mouseState[0] == 1:
                pygame.draw.rect(win, (255, 0, 0), (pygame.mouse.get_pos()[0] - dotSize / 2, pygame.mouse.get_pos()[1] - dotSize / 2, dotSize, dotSize))
        
            if mouseState[2] == 1:
                pygame.draw.rect(win, (0, 255, 0), (pygame.mouse.get_pos()[0] - dotSize / 2, pygame.mouse.get_pos()[1] - dotSize / 2, dotSize, dotSize))
            '''
        
            #Generates enemy spaceships randomly
            self.generationTimer += self.deltaTime
            if self.generationTimer >= self.timeBeforeGeneration:
                self.generationTimer = 0
                self.es = EnemySpaceship()
                self.enemySpaceship.add(self.es)
        
            #Checks for keyboard arrows to move the player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                if self.player.updateTimer >= self.player.updateTimerLimit:
                    if keys[pygame.K_LEFT]:
                        self.player.moveLeft()
                    if keys[pygame.K_RIGHT]:
                        self.player.moveRight()
                    if keys[pygame.K_UP]:
                        self.player.moveUp()
                    if keys[pygame.K_DOWN]:
                        self.player.moveDown()        
                    self.player.updateTimer = 0
                    
                self.player.updateTimer += 1
        
            #Clears the display with black color
            self.win.fill(BLACK)
        
            #Checks if a bullet must be destroyed (it reaches display boundaries)
            for pb in self.playerBulletList:
                if pb.mustDie() == True:
                    pb.kill()
        
            #Checks if the enemy spaceship must be destryoed (it reaches display boundaries)
            for es in self.enemySpaceship:
                if es.mustDie() == True:
                    es.kill()
        
            #Checks for each enemy and for each playerBullet if they collide
            for enemy in self.enemiesList:
                for playerBullet in self.playerBulletList:
                    if pygame.sprite.collide_rect(enemy, playerBullet):
                        playerBullet.kill()
                        enemy.damage(playerBullet.power)
                        if enemy.health <= 0:
                            self.score.add(enemy.scoreValue)
                            enemy.kill()
                            self.scoreText = "Score: " + str(self.score.score)
                            self.textSurface = self.myFont.render(self.scoreText, False, BLACK)
        
            #Checks for each enemy spaceship and for each playerBullet if they collide
            for es in self.enemySpaceship:
                for playerBullet in self.playerBulletList:
                    if pygame.sprite.collide_rect(es, playerBullet):
                        playerBullet.kill()
                        self.score.add(es.scoreValue)
                        es.kill()
                        self.scoreText = "Score: " + str(self.score.score)
                        self.textSurface = self.myFont.render(self.scoreText, False, BLACK)
                        
        
            #Checks if enemiesList reachs 0. If its the case, increase
            #the enemies counter and regenerates the enemcheckHighScoreies.
            if len(self.enemiesList) == 0:
                self.enemiesCount += 1
                self.__generateEnemies()
                
            #Checks if player and any of enemies collides
            for enemy in self.enemiesList:
                if pygame.sprite.collide_rect(enemy, self.player):
                    self.run = False
        
            #Updates enemies and player bullets
            self.enemiesList.update(self.deltaTime)
            self.playerBulletList.update(self.deltaTime)
            self.enemySpaceship.update(self.deltaTime)
            
            #draws stars
            for newStar in self.starsList:
                newStar.update();
                pygame.draw.rect(self.win, newStar.color, newStar.rect)
                
            #Draws player, enemies and player bullets
            self.all_sprites.draw(self.win)
            self.enemiesList.draw(self.win)
            self.playerBulletList.draw(self.win)
            self.enemySpaceship.draw(self.win)
        
            #Draws game Display
            pygame.draw.rect(self.win, self.gameDisplay.color, self.gameDisplay.rect)
            self.win.blit(self.textSurface, (DISPLAY_WIDTH_GAMEZONE + 1, 1))
        
            #Update the display (flip)
            pygame.display.update()
        
        self.score.checkHighScore(self.win)
        
        #Delete the reference to score object so its destructor is called
        self.score = ()
        
        #Function to generate enemies each time the enemiesCount reaches 0
		
    def __generateEnemies(self):
        for x in range(0, self.enemiesCount):
            self.enemy = Enemy()
            self.enemy.updateTimerLimit = randint(1, 10)
            self.enemy.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - self.enemy.rect.w)
            self.enemy.rect.y = randint(0, 10)
            self.enemiesList.add(self.enemy)
            
        for x in range(0, randint(0, self.enemiesCount + 2 / 2)):
            self.enemyBig = EnemyBig()
            self.enemyBig.updateTimerLimit = randint(1, 10)
            self.enemyBig.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - self.enemyBig.rect.w)
            self.enemyBig.rect.y = randint(0, 10)
            self.enemiesList.add(self.enemyBig)
