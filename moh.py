import pygame

import time
from random import randint

from PlayerMisc import *
from EnemyMisc import *
from EnvironmentMisc import *
from GameDisplay import *

from Util import *

from Score import *

'''
Initialization
'''
#Initializes pygame
pygame.init()

#Creates the game window
win = pygame.display.set_mode((DISPLAY_WIDTH_TOTAL, DISPLAY_HEIGHT_TOTAL))

#Set a title in the created window
display = pygame.display.set_caption("moh")

'''
Player
'''
#Group of sprites that represent the player
all_sprites = pygame.sprite.Group()

#Creates and initializes the player
player = Player()
player.rect.x = DISPLAY_WIDTH_GAMEZONE / 2
player.rect.y = DISPLAY_HEIGHT_GAMEZONE - player.rect.h
all_sprites.add(player)

'''
Player Bullets
'''
#Group of sprites that represent player bullets
playerBulletList = pygame.sprite.Group()

'''
Enemies
'''
#Group of sprites that represent enemies
enemiesList = pygame.sprite.Group()

#Keeps track of enemies amount
enemiesCount = 0

#Function to generate enemies each time the enemiesCount reaches 0
def generateEnemies():
    for x in range(0, enemiesCount):
        enemy = Enemy()
        enemy.updateTimerLimit = randint(1, 10)
        enemy.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - enemy.rect.w)
        enemy.rect.y = randint(0, 10)
        enemiesList.add(enemy)
        
    for x in range(0, randint(0, enemiesCount + 2 / 2)):
        enemyBig = EnemyBig()
        enemyBig.updateTimerLimit = randint(1, 10)
        enemyBig.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - enemyBig.rect.w)
        enemyBig.rect.y = randint(0, 10)
        enemiesList.add(enemyBig)

#Enemies spacesiphs: Generate randomly over time, they die when reach display boundaries

timeBeforeGeneration = randint(8000, 30000)
generationTimer = 0
        
enemySpaceship = pygame.sprite.Group()

'''
Stars
'''

starsList = []

for x in range(0, STARS_COUNT):
    star = Star(win)
    star.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE)
    star.rect.y = randint(0, DISPLAY_HEIGHT_GAMEZONE)
    starsList.append(star)

'''
GameDisplay
'''
gameDisplay = GameDisplay(win)

#Score number
score = Score()

#Game display score (text)
myFont = pygame.font.SysFont("Roboto", 50)
scoreText = "Score: 0"
textSurface = myFont.render(scoreText, False, BLACK)

'''
Game Loop
'''
#Sets the initial state of the main loop
run = True

before = pygame.time.get_ticks()
deltaTime = 0

#Main loop of the game
while run:
    
    deltaTime = pygame.time.get_ticks() - before
    #print (deltaTime)
    before = pygame.time.get_ticks()

    #Checks for user input, to exit from the game
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.updateTimer = player.updateTimerLimit
                
        if event.type == pygame.KEYDOWN:
            #Player shot
            if event.key == pygame.K_SPACE or event.key == pygame.K_LCTRL:
                if len(playerBulletList) < player.maxCurrentBullets:
                    playerBullet = PlayerBullet()
                    playerBullet.rect.x = player.rect.x + player.rect.width / 2 - playerBullet.rect.width / 2
                    playerBullet.rect.y = player.rect.y - playerBullet.rect.height
                    playerBulletList.add(playerBullet)
            if event.key == pygame.K_ESCAPE:
                run = False

    '''
    mouseState = pygame.mouse.get_pressed()

    if mouseState[0] == 1:
        pygame.draw.rect(win, (255, 0, 0), (pygame.mouse.get_pos()[0] - dotSize / 2, pygame.mouse.get_pos()[1] - dotSize / 2, dotSize, dotSize))

    if mouseState[2] == 1:
        pygame.draw.rect(win, (0, 255, 0), (pygame.mouse.get_pos()[0] - dotSize / 2, pygame.mouse.get_pos()[1] - dotSize / 2, dotSize, dotSize))
    '''

    #Generates enemy spaceships randomly
    generationTimer +=deltaTime
    if generationTimer >= timeBeforeGeneration:
        generationTimer = 0
        es = EnemySpaceship()
        enemySpaceship.add(es)

    #Checks for keyboard arrows to move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
        if player.updateTimer >= player.updateTimerLimit:
            if keys[pygame.K_LEFT]:
                player.moveLeft()
            if keys[pygame.K_RIGHT]:
                player.moveRight()
            if keys[pygame.K_UP]:
                player.moveUp()
            if keys[pygame.K_DOWN]:
                player.moveDown()        
            player.updateTimer = 0
            
        player.updateTimer += 1

    #Clears the display with black color
    win.fill((0, 0, 0))

    #Checks if a bullet must be destroyed (it reaches display boundaries)
    for pb in playerBulletList:
        if pb.mustDie() == True:
            pb.kill()

    #Checks if the enemy spaceship must be destryoed (it reaches display boundaries)
    for es in enemySpaceship:
        if es.mustDie() == True:
            es.kill()

    #Checks for each enemy and for each playerBullet if they collide
    for enemy in enemiesList:
        for playerBullet in playerBulletList:
            if pygame.sprite.collide_rect(enemy, playerBullet):
                playerBullet.kill()
                enemy.damage(playerBullet.power)
                if enemy.health <= 0:
                    score.add(enemy.scoreValue)
                    enemy.kill()
                    scoreText = "Score: " + str(score.score)
                    textSurface = myFont.render(scoreText, False, BLACK)

    #Checks for each enemy spaceship and for each playerBullet if they collide
    for es in enemySpaceship:
        for playerBullet in playerBulletList:
            if pygame.sprite.collide_rect(es, playerBullet):
                playerBullet.kill()
                score.add(es.scoreValue)
                es.kill()
                scoreText = "Score: " + str(score.score)
                textSurface = myFont.render(scoreText, False, BLACK)
                

    #Checks if enemiesList reachs 0. If its the case, increase
    #the enemies counter and regenerates the enemcheckHighScoreies.
    if len(enemiesList) == 0:
        enemiesCount += 1
        generateEnemies()
        
    #Checks if player and any of enemies collides
    for enemy in enemiesList:
        if pygame.sprite.collide_rect(enemy, player):
            run = False

    #Updates enemies and player bullets
    enemiesList.update(deltaTime)
    playerBulletList.update(deltaTime)
    enemySpaceship.update(deltaTime)
    
    #draws stars
    for newStar in starsList:
        newStar.update();
        pygame.draw.rect(win, newStar.color, newStar.rect)
        
    #Draws player, enemies and player bullets
    all_sprites.draw(win)
    enemiesList.draw(win)
    playerBulletList.draw(win)
    enemySpaceship.draw(win)

    #Draws game Display
    pygame.draw.rect(win, gameDisplay.color, gameDisplay.rect)
    win.blit(textSurface, (DISPLAY_WIDTH_GAMEZONE + 1, 1))

    #Update the display (flip)
    pygame.display.update()

#score.checkHighScores()
print (score.score)

#Quits the application
pygame.quit()
