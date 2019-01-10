import pygame
import sqlite3

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
            
    def checkHighScore(self):
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

                self.playerName = input("Ingrese su nombre: ")

                if not self.playerName == "":
                    self.cursor.execute("INSERT INTO SCORES(player_name, score) VALUES(?, ?)", [self.playerName, self.score])
                    self.connection.commit()

    def add(self, scoreToAdd):
        self.score += scoreToAdd

    def __del__(self):
        print ("Chau mundo")
        self.connection.close()
