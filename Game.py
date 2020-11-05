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
        self.bulletsFired = 0
        self.bulletsHit = 0
        
        '''
        Enemies
        '''
        #Group of sprites that represent enemies
        self.enemiesList = pygame.sprite.Group()
        self.enemyFormationDirection = 0

        self.enemyFormationTimer = 0

        self.enemyTimerLimit = 0
        self.enemyTimer = 0
        
        #Keeps track of stage
        self.stage = 1

        #Enemies bullets
        self.enemyBulletsList = pygame.sprite.Group()
        
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

        self.timerBeforeNewStageLimit = 3000
        self.timerBeforeNewStage = 0
        
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
                self.__handlePauseEvents(events)
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
                            self.bulletsFired += 1
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
        
            #Checks for keyboard arrows to move the player
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.player.move(keys, self.deltaTime)
        
            #Checks for each enemy and for each playerBullet if they collide
            for enemy in self.enemiesList:
                for playerBullet in self.playerBulletList:
                    if pygame.sprite.collide_rect(enemy, playerBullet):
                        self.animations.append(Animation(SP_player_bullet, playerBullet.rect, 20))
                        playerBullet.kill()
                        self.bulletsHit += 1
                        enemy.damage(playerBullet.power)
                        if enemy.health <= 0:
                            self.score.add(enemy.scoreValue)
                            if (enemy.tag == "spaceship"):
                                self.animations.append(Animation(SP_enemy_spaceship, enemy.rect, 100, 5))
                            else:
                                self.animations.append(Animation(SP_enemy_normal_explotion, enemy.rect, 100))
                            self.scoreText = "Score: " + str(self.score.score)
                            self.textSurface = self.myFont.render(self.scoreText, False, BLACK)
        
            #Checks if enemiesList reachs 0. If its the case, increase
            #the enemies counter and regenerates the enemies.
                    
            if len(self.enemiesList) == 0:

                #self.timerBeforeNewStage += self.deltaTime
                #if (self.timerBeforeNewStage >= self.timerBeforeNewStageLimit):
                #self.timerBeforeNewStage = 0
                self.__generateEnemies()
                self.stage += 1

            #Checks if player and any of enemies collides
            for enemy in self.enemiesList:
                if pygame.sprite.collide_rect(enemy, self.player):
                    self.run = False

            #Checks if any enemy bullet collides against player
            for enemyBullet in self.enemyBulletsList:
                if pygame.sprite.collide_rect(enemyBullet, self.player):
                    self.run = False
        
            #Updates enemies and player bullets
            self.enemiesList.update(self.deltaTime, self.enemyBulletsList)
            self.playerBulletList.update(self.deltaTime)

            # Enemy formation direction and movement (as a group)
            for enemy in self.enemiesList:
                if (self.__getReachedLeft(self.enemiesList)):
                    self.enemyFormationDirection = 1
                elif (self.__getReachedRight(self.enemiesList)):
                    self.enemyFormationDirection = 0

            #Updates enemy formation 
            self.enemyFormationTimer += self.deltaTime
            if (self.enemyFormationTimer >= FORMATION_LIMIT_TIMER):
                for enemy in self.enemiesList:
                    if (self.enemyFormationDirection == 0):
                        enemy.targetPosition.x -= 1
                    else:
                        enemy.targetPosition.x += 1

                self.enemyFormationTimer = 0

            #Updates stars positions
            for star in self.starsList:
                star.update(self.deltaTime)

            #Updates enemy bullets positions
            for enemyBullet in self.enemyBulletsList:
                enemyBullet.update(self.deltaTime)

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
                self.timerBeforeRefresh = 0

                for star in self.starsList:
                    pygame.draw.rect(self.win, star.color, star.rect)

                self.all_sprites.draw(self.win)
                self.enemiesList.draw(self.win)
                self.playerBulletList.draw(self.win)
                self.enemyBulletsList.draw(self.win)

                '''
                Anims
                '''
                self.animGroup = pygame.sprite.Group()
                for anim in self.animations:
                    self.animGroup.add(anim.getCurrentSprite())
                self.animGroup.draw(self.win)
        
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

        contador = 0    

        playerRect = pygame.sprite.Rect(0, 0, 0, 0)

        for player in self.all_sprites:
            playerRect = player.rect

        for x in range(8):
            for y in range(4):
                contador += 1

                self.enemy = EnemyNormal(playerRect)
                self.enemy.updateTimerLimit = 5
                side = randint(0, 1)
                if side == 0:
                    self.enemy.rect.x = -self.enemy.anim.getCurrentSprite().rect.w - contador * (self.enemy.anim.getCurrentSprite().rect.w - 10) 
                else:
                    self.enemy.rect.x = DISPLAY_WIDTH_GAMEZONE + 1 + contador * (self.enemy.anim.getCurrentSprite().rect.w + 10) 
                
                self.enemy.rect.y = randint(0, DISPLAY_HEIGHT_GAMEZONE / 2)

                self.enemy.targetPosition.x = x * 60 + 50
                self.enemy.targetPosition.y = y * 40 + 50

                self.enemy.calculateFormationLimits()

                self.enemiesList.add(self.enemy)

    def __handlePauseEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = False
                if event.key == pygame.K_ESCAPE:
                    self.run = False

    def __getReachedRight(self, enemiesList):
        result = False
        for enemy in enemiesList:
            if (enemy.targetPosition.x + enemy.anim.getCurrentSprite().rect.w >= DISPLAY_WIDTH_GAMEZONE):
                result = True
                break

        return result

    def __getReachedLeft(self, enemiesList):
        result = False
        for enemy in enemiesList:
            if (enemy.targetPosition.x <= 0):
                result = True
                break

        return result