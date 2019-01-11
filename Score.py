import pygame
import sqlite3

from tkinter import *
from Util import *

class Score:
    def __init__(self):
        self.score = 0
        self.highScoreLimitToStore = 10

        self.connection = sqlite3.connect("scores.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS SCORES(score_id INTEGER PRIMARY KEY, player_name TEXT, score INTEGER)")

        self.cursor.execute("SELECT * FROM SCORES")

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
                
                charTexts = ["a", "a", "a", "a", "a"]
                textNameLetters = [myFont.render("a", False, GREEN),
                                   myFont.render("a", False, WHITE),
                                   myFont.render("a", False, WHITE),
                                   myFont.render("a", False, WHITE),
                                   myFont.render("a", False, WHITE)]

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
                                self.playerName = charTexts[0] + charTexts[1] + charTexts[2] + charTexts[3] + charTexts[4]
                                runScoreWindow = False
                                
                            #Changes the focused letter spaced
                            if event.key == pygame.K_LEFT:
                                if chosenLetter == 0:
                                    chosenLetter = len(textNameLetters) - 1
                                else:
                                    chosenLetter -= 1

                                chosenChar = allChars.index(charTexts[chosenLetter])

                                if chosenLetter == 0:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, GREEN)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 1:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, GREEN)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 2:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, GREEN)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 3:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, GREEN)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 4:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, GREEN)
                                
                            if event.key == pygame.K_RIGHT:
                                if chosenLetter == len(textNameLetters) - 1:
                                    chosenLetter = 0
                                else:
                                    chosenLetter += 1

                                chosenChar = allChars.index(charTexts[chosenLetter])
                                
                                if chosenLetter == 0:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, GREEN)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 1:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, GREEN)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 2:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, GREEN)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 3:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, GREEN)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 4:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, GREEN)
                                    
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
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 1:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, GREEN)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 2:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, GREEN)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 3:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, GREEN)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 4:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, GREEN)
                                    
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
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 1:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, GREEN)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 2:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, GREEN)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 3:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, GREEN)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, WHITE)
                                elif chosenLetter == 4:
                                    textNameLetters[0] = myFont.render(charTexts[0], False, WHITE)
                                    textNameLetters[1] = myFont.render(charTexts[1], False, WHITE)
                                    textNameLetters[2] = myFont.render(charTexts[2], False, WHITE)
                                    textNameLetters[3] = myFont.render(charTexts[3], False, WHITE)
                                    textNameLetters[4] = myFont.render(charTexts[4], False, GREEN)

                                    
                    win.fill(BLACK)
                    
                    win.blit(textNameLetters[0], (DISPLAY_WIDTH_GAMEZONE / 2, DISPLAY_HEIGHT_GAMEZONE / 2))
                    win.blit(textNameLetters[1], (DISPLAY_WIDTH_GAMEZONE / 2 + 35, DISPLAY_HEIGHT_GAMEZONE / 2))
                    win.blit(textNameLetters[2], (DISPLAY_WIDTH_GAMEZONE / 2 + 70, DISPLAY_HEIGHT_GAMEZONE / 2))
                    win.blit(textNameLetters[3], (DISPLAY_WIDTH_GAMEZONE / 2 + 105, DISPLAY_HEIGHT_GAMEZONE / 2))
                    win.blit(textNameLetters[4], (DISPLAY_WIDTH_GAMEZONE / 2 + 140, DISPLAY_HEIGHT_GAMEZONE / 2))

                    #Update the display (flip)
                    pygame.display.update()
                    

                if not self.playerName == "":
                    self.cursor.execute("INSERT INTO SCORES(player_name, score) VALUES(?, ?)", [self.playerName, self.score])
                    self.connection.commit()

    def showHighScores(self, win):

        self.playerName = ""

        #Game display letrers (text)
        fontTitle = pygame.font.SysFont("Roboto", 70)
        myFont = pygame.font.SysFont("Roboto", 50)

        #For menu title
        highScoresTitle = fontTitle.render("High Scores", False, WHITE)

        #For scores display
        textNames = [myFont.render("", False, WHITE),
                     myFont.render("", False, WHITE),
                     myFont.render("", False, WHITE),
                     myFont.render("", False, WHITE),
                     myFont.render("", False, WHITE),
                     myFont.render("", False, WHITE),
                     myFont.render("", False, WHITE),
                     myFont.render("", False, WHITE),
                     myFont.render("", False, WHITE),
                     myFont.render("", False, WHITE)]
        textScores = [myFont.render("", False, WHITE),
                      myFont.render("", False, WHITE),
                      myFont.render("", False, WHITE),
                      myFont.render("", False, WHITE),
                      myFont.render("", False, WHITE),
                      myFont.render("", False, WHITE),
                      myFont.render("", False, WHITE),
                      myFont.render("", False, WHITE),
                      myFont.render("", False, WHITE),
                      myFont.render("", False, WHITE)]
        
        self.cursor.execute("SELECT * FROM SCORES")

        self.allFetched = self.cursor.fetchall()

        self.allFetched.sort(key=lambda tup: tup[2], reverse=True)

        x = 0
        for highScore in self.allFetched:
            textNames[x] = myFont.render(highScore[1], False, WHITE)
            textScores[x] = myFont.render(str(highScore[2]), False, WHITE)
            x += 1
                
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
            
            win.fill(BLACK)

            win.blit(highScoresTitle, (DISPLAY_WIDTH_TOTAL / 3, DISPLAY_HEIGHT_TOTAL / 9 - 40))
            x = 0
            for tn in textNames:
                win.blit(tn, (DISPLAY_WIDTH_TOTAL / 2 - 90, DISPLAY_HEIGHT_TOTAL / 5 + x * 40))
                x += 1
                
            x = 0
            for ts in textScores:
                win.blit(ts, (DISPLAY_WIDTH_TOTAL / 2 + 40, DISPLAY_HEIGHT_TOTAL / 5 + x * 40))
                x += 1

            #Update the display (flip)
            pygame.display.update()

    def add(self, scoreToAdd):
        self.score += scoreToAdd

    def __del__(self):
        self.connection.close()
