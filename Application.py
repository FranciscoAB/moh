import pygame
import time

from Util import *
from Game import *

class Application:

    def __init__(self):
		#Initializes pygame
        pygame.init()
		
		#Creates the game window
        self.win = pygame.display.set_mode((DISPLAY_WIDTH_TOTAL, DISPLAY_HEIGHT_TOTAL))
        
        #Set a title in the created window
        self.display = pygame.display.set_caption("moh")
        
        
        #Sets the initial state of the user input (menu)
        self.option = 1
        
        #Sets the initial state of the main loop
        self.run = True
        
        #Used to slow down the ejecution
        self.before = pygame.time.get_ticks()
        self.deltaTime = 0
        
        self.colorDeMierda = (123, 34, 200)
        
        #Texts
        self.myFont = pygame.font.SysFont("Roboto", 60)
        self.textSurfacePlay = self.myFont.render("Play!", False, self.colorDeMierda)
        self.textSurfaceHighScores = self.myFont.render("High Scores", False, WHITE)
        self.textSurfaceQuit = self.myFont.render("Quit", False, WHITE)
		
    def loop(self):
        
        #Main loop of the Application
        while self.run:
        
            self.deltaTime = pygame.time.get_ticks() - self.before
            self.before = pygame.time.get_ticks()
        
            #Checks for user input, to chose an option from menu
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                    if event.key == pygame.K_UP:
                        if self.option <= 1:
                            self.option = 3
                        else:
                            self.option -= 1
                    if event.key == pygame.K_DOWN:
                        if self.option >= 3:
                            self.option = 1
                        else:
                            self.option += 1
                    #Updates the text color
                    if self.option == 1:
                        self.textSurfacePlay = self.myFont.render("Play!", False, self.colorDeMierda)
                        self.textSurfaceHighScores = self.myFont.render("High Scores", False, WHITE)
                        self.textSurfaceQuit = self.myFont.render("Quit", False, WHITE)
                    elif self.option == 2:
                        self.textSurfacePlay = self.myFont.render("Play!", False, WHITE)
                        self.textSurfaceHighScores = self.myFont.render("High Scores", False, self.colorDeMierda)
                        self.textSurfaceQuit = self.myFont.render("Quit", False, WHITE)
                    elif self.option == 3:
                        self.textSurfacePlay = self.myFont.render("Play!", False, WHITE)
                        self.textSurfaceHighScores = self.myFont.render("High Scores", False, WHITE)
                        self.textSurfaceQuit = self.myFont.render("Quit", False, self.colorDeMierda)
                            
                    if event.key == pygame.K_RETURN:
                        if self.option == 1: #The game starts
                            game = Game(self.win)
                            game.loop()
                            game = ()
                            
                        elif self.option == 2: #Display with high-scores shows
                            print("gonna show high-scores")
                        elif self.option == 3: #Quits the game
                            self.run = False
                            
                #Clears the display with black color
                self.win.fill(BLACK)
        
                #Draws game Display 
                self.win.blit(self.textSurfacePlay, (DISPLAY_WIDTH_GAMEZONE / 2, 200))
                self.win.blit(self.textSurfaceHighScores, (DISPLAY_WIDTH_GAMEZONE / 2, 300))
                self.win.blit(self.textSurfaceQuit, (DISPLAY_WIDTH_GAMEZONE / 2, 400))
                
                #Update the display (flip)
                pygame.display.update()			
    
        #Quits the application
        pygame.quit()