import pygame
import time
from random import randint

from PlayerMisc import *
from EnemyMisc import *
from EnvironmentMisc import *
from GameDisplay import *

from Util import *

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
        enemy.rect.x = randint(0, DISPLAY_WIDTH_GAMEZONE - enemy.rect.w)
        enemy.rect.y = randint(0, 10)
        enemiesList.add(enemy)

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
score = 0

#Game display score (text)
myFont = pygame.font.SysFont("Roboto", 50)
scoreText = "Score: 0"
textSurface = myFont.render(scoreText, False, BLACK)

'''
Game Loop
'''
#Sets the initial state of the main loop
run = True

#Main loop of the game
while run:

    #Delay to make the game slower (arreglar esto con FPSs)
    pygame.time.delay(4)

    #Checks for user input, to exit from the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    '''
    mouseState = pygame.mouse.get_pressed()

    if mouseState[0] == 1:
        pygame.draw.rect(win, (255, 0, 0), (pygame.mouse.get_pos()[0] - dotSize / 2, pygame.mouse.get_pos()[1] - dotSize / 2, dotSize, dotSize))

    if mouseState[2] == 1:
        pygame.draw.rect(win, (0, 255, 0), (pygame.mouse.get_pos()[0] - dotSize / 2, pygame.mouse.get_pos()[1] - dotSize / 2, dotSize, dotSize))
    '''

    #Checks for keyboard arrows to move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.moveLeft()
        
    if keys[pygame.K_RIGHT]:
        player.moveRight()
        
    if keys[pygame.K_UP]:
        player.moveUp()
        
    if keys[pygame.K_DOWN]:
        player.moveDown()
        
    if keys[pygame.K_ESCAPE]:
        run = False

    #Player shot
    if keys[pygame.K_SPACE]:
        if len(playerBulletList) == 0:
            playerBullet = PlayerBullet()
            playerBullet.rect.x = player.rect.x + player.rect.width / 2 - playerBullet.rect.width / 2
            playerBullet.rect.y = player.rect.y - playerBullet.rect.height
            playerBulletList.add(playerBullet)

    #Clears the display with black color
    win.fill((0, 0, 0))

    #Checks if a bullet must be destroyed (it reaches display boundaries)
    for pb in playerBulletList:
        if pb.mustDie() == True:
            pb.kill()

    #Checks for each enemy and for each playerBullet if they collide
    for enemy in enemiesList:
        for playerBullet in playerBulletList:
            if pygame.sprite.collide_rect(enemy, playerBullet):
                enemy.kill()
                playerBullet.kill()
                score += 1
                scoreText = "Score: " + str(score)
                textSurface = myFont.render(scoreText, False, BLACK)

    #Checks if enemiesList reachs 0. If its the case, increase
    #the enemies counter and regenerates the enemies.
    if len(enemiesList) == 0:
        enemiesCount += 1
        generateEnemies()
        
    #Checks if player and any of enemies collides
    for enemy in enemiesList:
        if pygame.sprite.collide_rect(enemy, player):
            print ("Score:", score)
            run = False

    #Updates enemies and player bullets
    enemiesList.update()
    playerBulletList.update()
    
    #draws stars
    for newStar in starsList:
        newStar.update();
        pygame.draw.rect(win, newStar.color, newStar.rect)
        
    #Draws player, enemies and player bullets
    all_sprites.draw(win)
    enemiesList.draw(win)
    playerBulletList.draw(win)

    #Draws game Display
    pygame.draw.rect(win, gameDisplay.color, gameDisplay.rect)
    win.blit(textSurface, (DISPLAY_WIDTH_GAMEZONE + 1, 1))

    #Update the display (flip)
    pygame.display.update()

#Quits the application
pygame.quit()
