import pygame
import pygame_textinput
import os.path

class Score:
    def __init__(self):
        self.score = 0
        self.highScoreLimitToStore = 10

        self.currentStoredScores = 0

        if not os.path.isfile("high_scores.txt"):
            file = open("high_scores.txt", "a+")
            file.write("00;")
            
    def checkHighScore(self):
        score = 0

    def add(self, scoreToAdd):
        self.score += scoreToAdd

    def checkHighScores(self):
        
        file = open("high_scores.txt", "r")

        highScores = file.read()

        auxString = ""
        index = 0
        
        for x in highScores:
            if x == ";":
                index += 1
                auxString = ""
            else:
                auxString += x
                
        
        file.close()
