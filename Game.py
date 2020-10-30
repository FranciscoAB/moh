import pygame

import time
from random import randint

from PlayerMisc import *
from EnemyMisc import *
from EnvironmentMisc import *
from GameDisplay import *

from Util import *

from Score import *

from Animation import *
from SpritesData import *

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
        Animations
        '''
        self.animations = []
        #El grupo es necesario por la funcion draw()
        self.animGroup = pygame.sprite.Group()

        '''
        Game Loop
        '''
        #Sets the initial state of the main loop
        self.run = True

        self.pause = False
        
        self.getTicksLastFrame = 0
        self.deltaTime = 0
        
        self.timeBeforeRefresh = 7
        self.timerBeforeRefresh = 0
        
	#Main loop of the game
    def loop(self):
        while self.run:

            t = pygame.time.get_ticks()
            self.deltaTime = (t - self.getTicksLastFrame)
            self.getTicksLastFrame = t

            self.timerBeforeRefresh += self.deltaTime

            #Checks for user input, to exit from the game
            events = pygame.event.get()
            '''''''''''''''''''''''''''''''''''''''
            PAUSE!!!!!
            '''''''''''''''''''''''''''''''''''''''
            if self.pause:
                self.handlePauseEvents(events)
                continue

            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = True
                        continue

                    #Player shot
                    if event.key == pygame.K_SPACE or event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        if len(self.playerBulletList) < self.player.maxCurrentBullets:
                            self.playerBullet = PlayerBullet()
                            self.playerBullet.rect.x = self.player.rect.x + self.player.rect.width / 2 - self.playerBullet.rect.width / 2
                            self.playerBullet.rect.y = self.player.rect.y - self.playerBullet.rect.height
                            self.playerBulletList.add(self.playerBullet)
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
        
            #TODO VER ESTO
            #Generates enemy spaceships randomly
            self.generationTimer += self.deltaTime
            if self.generationTimer >= self.timeBeforeGeneration:
                self.generationTimer = 0
                self.es = EnemySpaceship()
                self.enemySpaceship.add(self.es)
        
            #Checks for keyboard arrows to move the player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.player.move(keys, self.deltaTime)
        
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
                        self.animations.append(Animation(SP_player_bullet, playerBullet, 20))
                        playerBullet.kill()
                        enemy.damage(playerBullet.power)
                        if enemy.health <= 0:
                            self.score.add(enemy.scoreValue)
                            self.animations.append(Animation(SP_enemy_normal, enemy, 100))
                            enemy.kill()
                            self.scoreText = "Score: " + str(self.score.score)
                            self.textSurface = self.myFont.render(self.scoreText, False, BLACK)

            #Checks for each enemy spaceship and for each playerBullet if they collide
            for es in self.enemySpaceship:
                for playerBullet in self.playerBulletList:
                    if pygame.sprite.collide_rect(es, playerBullet):
                        self.animations.append(Animation(SP_player_bullet, playerBullet, 20))
                        playerBullet.kill()
                        self.score.add(es.scoreValue)
                        self.animations.append(Animation(SP_enemy_spaceship, es, 100))
                        es.kill()
                        self.scoreText = "Score: " + str(self.score.score)
                        self.textSurface = self.myFont.render(self.scoreText, False, BLACK)
                        
        
            #Checks if enemiesList reachs 0. If its the case, increase
            #the enemies counter and regenerates the enemies.
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
            
            #Updates stars positions
            for star in self.starsList:
                star.update(self.deltaTime)

            #Updates Animations
            auxAnimList = []
            for anim in self.animations:
                if not anim.shouldDie:
                    auxAnimList.append(anim)
                anim.update(self.deltaTime)
            self.animations = auxAnimList
            
            #Clears the display with black color
            self.win.fill(BLACK)
            
            #Draws player, enemies, player bullets and stars
            if (self.timerBeforeRefresh >= self.timeBeforeRefresh):
                for star in self.starsList:
                    pygame.draw.rect(self.win, star.color, star.rect)

                self.all_sprites.draw(self.win)
                self.enemiesList.draw(self.win)
                self.playerBulletList.draw(self.win)
                self.enemySpaceship.draw(self.win)

                '''
                Anims
                '''
                self.animGroup = pygame.sprite.Group()
                for anim in self.animations:
                    self.animGroup.add(anim.getCurrentSprite())
                self.animGroup.draw(self.win)
                
                self.timerBeforeRefresh = 0
        
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
            self.enemy = EnemyNormal()
            self.enemy.updateTimerLimit = randint(2, 9)
            self.enemy.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - self.enemy.rect.w)
            self.enemy.rect.y = randint(0, 10)
            self.enemiesList.add(self.enemy)

        for x in range(0, randint(0, (int)((self.enemiesCount + 2) / 2))):
            self.enemyBig = EnemyBig()
            self.enemyBig.updateTimerLimit = randint(2, 9)
            self.enemyBig.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - self.enemyBig.rect.w)
            self.enemyBig.rect.y = randint(0, 10)
            self.enemiesList.add(self.enemyBig)

    def handlePauseEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = False
                if event.key == pygame.K_ESCAPE:
                    self.run = False