import pygame
import sqlite3

from tkinter import *
from Util import *

class Score:
    def __init__(self):
        self.score = 0
        self.highScoreLimitToStore = 3

        self.connection = sqlite3.connect("scores.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS SCORES(score_id INTEGER PRIMARY KEY, player_name TEXT, score INTEGER)")

        self.cursor.execute("SELECT * FROM SCORES")

        print (self.cursor.fetchall())

        self.playerName = ""

    def checkHighScore(self, win):
        if self.score > 0:
            self.cursor.execute("SELECT * FROM SCORES")

            self.itsHighScore = False

            self.allFetched = self.cursor.fetchall()

            #Will check if the high score pool is full, if its the case,
            #delete de lowest score and load the new one
            #If the pool is not full, then the score gonna be stored.
            if len(self.allFetched) >= self.highScoreLimitToStore:
                for [scoreId, playerName, score] in self.allFetched:
                    #If true, then the score its a high score and must be stored
                    if self.score > score:
                        self.itsHighScore = True
                        break
                
                self.lowestScoreFetch = min(self.allFetched, key=lambda item: item[2])
                self.cursor.execute("DELETE FROM SCORES WHERE score_id=?", [self.lowestScoreFetch[0]])
            else:
                self.itsHighScore = True
            
            if self.itsHighScore == True:

                self.playerName = ""

                #Game display letrers (text)
                myFont = pygame.font.SysFont("Roboto", 50)

                charText1 = "a"
                charText2 = "a"
                charText3 = "a"
                
                textName1 = myFont.render(charText1, False, GREEN)
                textName2 = myFont.render(charText2, False, WHITE)
                textName3 = myFont.render(charText3, False, WHITE)
                
                charTexts = [charText1, charText2, charText3]
                textNameLetters = [textName1, textName2, textName3]

                allChars = [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]

                chosenLetter = 0
                chosenChar = 1
                totalChars = len(allChars)
                
                runScoreWindow = True

                while runScoreWindow == True:

                    #Checks for user input, to exit from the game
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            runScoreWindow = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                runScoreWindow = False
                            if event.key == pygame.K_RETURN:
                                self.playerName = charTexts[0] + charTexts[1] + charTexts[2]
                                runScoreWindow = False
                                
                            #Changes the focused letter spaced
                            if event.key == pygame.K_LEFT:
                                if chosenLetter == 0:
                                    chosenLetter = 2
                                else:
                                    chosenLetter -= 1

                                if chosenLetter == 0:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, GREEN)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                elif chosenLetter == 1:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, GREEN)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                elif chosenLetter == 2:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, GREEN)
                                
                            if event.key == pygame.K_RIGHT:
                                if chosenLetter == 2:
                                    chosenLetter = 0
                                else:
                                    chosenLetter += 1                            

                                if chosenLetter == 0:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, GREEN)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                elif chosenLetter == 1:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, GREEN)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                elif chosenLetter == 2:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, GREEN)
                                    
                            #Changes the char for each letter space
                            if event.key == pygame.K_UP:
                                if chosenChar < totalChars - 1:
                                    chosenChar += 1
                                else:
                                    chosenChar = 0

                                charTexts[chosenLetter] = allChars[chosenChar] 
                                    
                                textNameLetters[chosenLetter] = myFont.render(charTexts[chosenLetter], False, GREEN)

                                if chosenLetter == 0:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, GREEN)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                elif chosenLetter == 1:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, GREEN)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                elif chosenLetter == 2:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, GREEN)
                                    
                            if event.key == pygame.K_DOWN:
                                if chosenChar > 0:
                                    chosenChar -= 1
                                else:
                                    chosenChar = totalChars - 1
                                
                                charTexts[chosenLetter] = allChars[chosenChar] 
                                    
                                textNameLetters[chosenLetter] = myFont.render(allChars[chosenChar], False, GREEN)

                                if chosenLetter == 0:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, GREEN)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                elif chosenLetter == 1:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, GREEN)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                elif chosenLetter == 2:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, GREEN)

                                    
                    win.fill(BLACK)
                    
                    win.blit(textNameLetters[0], (DISPLAY_WIDTH_GAMEZONE / 2, DISPLAY_HEIGHT_GAMEZONE / 2))
                    win.blit(textNameLetters[1], (DISPLAY_WIDTH_GAMEZONE / 2 + 35, DISPLAY_HEIGHT_GAMEZONE / 2))
                    win.blit(textNameLetters[2], (DISPLAY_WIDTH_GAMEZONE / 2 + 70, DISPLAY_HEIGHT_GAMEZONE / 2))

                    #Update the display (flip)
                    pygame.display.update()
                    

                if not self.playerName == "":
                    self.cursor.execute("INSERT INTO SCORES(player_name, score) VALUES(?, ?)", [self.playerName, self.score])
                    self.connection.commit()

    def add(self, scoreToAdd):
        self.score += scoreToAdd

    def __del__(self):
        print ("Chau mundo")
        self.connection.close()
