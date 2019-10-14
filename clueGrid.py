import csv

import clueUtils
import guess

class clueGrid:
    def __init__(self):
        self.grid = []
        
        numPlayers = clueUtils.numPlayers
        numSuspects = clueUtils.numSuspects
        numWeapons = clueUtils.numWeapons
        numRooms = clueUtils.numRooms
        numCards = clueUtils.numCards
        numPlayerCards = clueUtils.numPlayerCards
        
        for i in range(numSuspects):
            suspectRow = []
            for j in range(numPlayers):
                suspectRow.append(numPlayerCards[j]/numCards)
            suspectRow.append(1/numSuspects)
            self.grid.append(suspectRow)
        for i in range(numWeapons):
            weaponRow = []
            for j in range(numPlayers):
                weaponRow.append(numPlayerCards[j]/numCards)
            weaponRow.append(1/numWeapons)
            self.grid.append(weaponRow)
        for i in range(numRooms):
            roomRow = []
            for j in range(numPlayers):
                roomRow.append(numPlayerCards[j]/numCards)
            roomRow.append(1/numRooms)
            self.grid.append(roomRow)
    
    def show(self, playerName, card):
        cardIndex = clueUtils.allCards.index(card)
        playerIndex = clueUtils.playerNames.index(playerName)
        self.grid[cardIndex][playerIndex] = 1
        
    def playerPassed(self, playerName, theGuess):
        playerIndex = clueUtils.playerNames.index(playerName)
        cards = theGuess.cardList()
        for card in cards:
            cardIndex = allCards.index(card)
            self.grid[cardIndex][playerIndex] = 0
    
    def readGuessLog(self):
        with open("guessLogTest.csv") as csvfile:
            csvReader = csv.reader(csvfile)
            header = True
            for row in csvReader:
                if header:
                    #do nothing
                    header = False
                else:
                    print(row)
                    self.processGuessLogRow(row)
                    
    def processGuessLogRow(self, row):
        suspect = row[0]
        weapon = row[1]
        room = row[2]
        
    
    def display(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                print("%8.2f" % (self.grid[i][j]), end='')
                
            print("\n")

#Test code
if __name__ == "__main__":
    myTestGrid = clueGrid()
    myTestGrid.display()
    myTestGrid.readGuessLog()
#   print(clueUtils.numPlayerCards)
