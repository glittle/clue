import csv

import clueUtils
import guess

suspects = clueUtils.suspects
weapons = clueUtils.weapons
rooms = clueUtils.rooms
allCards = clueUtils.allCards

playerNames = clueUtils.playerNames

numPlayers = clueUtils.numPlayers
numSuspects = clueUtils.numSuspects
numWeapons = clueUtils.numWeapons
numRooms = clueUtils.numRooms
numCards = clueUtils.numCards
numPlayerCards = clueUtils.numPlayerCards
mysteryIndex = numPlayers

epsilon = 0.0001

class clueGrid:
    def __init__(self):
        self.grid = []
        
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
    
    def at(self, card, playerName):
        cardIndex = clueUtils.allCards.index(card)
        if playerName == "mystery":
            playerIndex = mysteryIndex
        else:
            playerIndex = clueUtils.playerNames.index(playerName)
        return self.grid[cardIndex][playerIndex]
    
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
        with open("public/guessLog.csv") as csvfile:
            csvReader = csv.reader(csvfile)
            header = True
            for row in csvReader:
                if header:
                    #do nothing
                    header = False
                else:
                    #print(row)
                    self.processGuessLogRow(row)
    
    def readPrivateLog(self, filename):
        with open(filename) as csvfile:
            csvReader = csv.reader(csvfile)
            for row in csvReader:
                self.processPrivateLogRow(row)
                
    def processPrivateLogRow(self, row):
        playerName = row[0]
        card = row[1]
        playerIndex = clueUtils.playerNames.index(playerName)
        cardIndex = clueUtils.allCards.index(card)
        self.grid[cardIndex][playerIndex] = 1
        self.updateCardProbability(cardIndex)

    def processGuessLogRow(self, row):
        suspect = row[0]
        weapon = row[1]
        room = row[2]
        suspectIndex = clueUtils.allCards.index(suspect)
        weaponIndex = clueUtils.allCards.index(weapon)
        roomIndex = clueUtils.allCards.index(room)
        playerResponses = []
        for playerIndex in range(clueUtils.numPlayers):
            colIndex = playerIndex + 3
            playerResponse = row[colIndex]
            playerResponses.append(playerResponse)
            if playerResponse == "passed":
                self.grid[suspectIndex][playerIndex] = 0
                self.grid[weaponIndex][playerIndex] = 0
                self.grid[roomIndex][playerIndex] = 0
            elif playerResponse == "showed":
                if (self.grid[suspectIndex][playerIndex] == 0) and (self.grid[weaponIndex][playerIndex] == 0):
                    self.grid[roomIndex][playerIndex] = 1
                elif (self.grid[suspectIndex][playerIndex] == 0) and (self.grid[roomIndex][playerIndex] == 0):
                    self.grid[weaponIndex][playerIndex] = 1
                elif (self.grid[weaponIndex][playerIndex] == 0) and (self.grid[roomIndex][playerIndex] == 0):
                    self.grid[suspectIndex][playerIndex] = 1
    
    def updateCardProbability(self, cardIndex):
        # Return False unless something is changed
        changedSomething = False
        
        # Set all other probabilities to zero if owner is known
        for playerIndex in range(numPlayers + 1):
            value = self.grid[cardIndex][playerIndex]
            if value == 1:
                for i in range(numPlayers + 1):
                    if (i != playerIndex) and (self.grid[cardIndex][i] != 0):
                        self.grid[cardIndex][i] = 0
                        changedSomething = True
                return changedSomething
        
        # Sum probabilities
        sumOfProbabilities = 0
        for playerIndex in range(numPlayers + 1):
            value = self.grid[cardIndex][playerIndex]
            sumOfProbabilities = sumOfProbabilities + value
        
        # Check for invalid condition
        if sumOfProbabilities == 0:
            print("Error: Zero probability for %s" % (clueUtils.allCards[cardIndex]))
            return changedSomething
            
        # Update probabilities so all nonzero probabilities add up to one
        for playerIndex in range(numPlayers + 1):
            value = self.grid[cardIndex][playerIndex]
            newValue = value/sumOfProbabilities
            if ((newValue - value) >= 0.0001):
                self.grid[cardIndex][playerIndex] = newValue
                changedSomething = True
        return changedSomething
    
    def updateCardProbabilities(self):
        loopCount = 0
        while True:
            loopCount = loopCount + 1
            changedCount = 0
            for cardIndex in range(clueUtils.numCards):
                changedSomething = self.updateCardProbability(cardIndex)
                if changedSomething == True:
                    changedCount = changedCount + 1
            if changedCount == 0:
                break
            if loopCount >= 100:
                break
            self.ifAllPlayerCardsKnownPlayerDoesNotHaveAnyOtherCards()
        return loopCount
    
    def knownPlayerCards(self, playerName):
        knownHand = []
        for card in allCards:
            if self.at(card, playerName) == 1:
                knownHand.append(card)
        return knownHand
    
    def ifAllPlayerCardsKnownPlayerDoesNotHaveAnyOtherCards(self):
        for playerName in playerNames:
            playerIndex = playerNames.index(playerName)
            knownCardsInPlayerHand = self.knownPlayerCards(playerName)
            if len(knownCardsInPlayerHand) == numPlayerCards[playerIndex]:
                for card in allCards:
                    cardIndex = allCards.index(card)
                    if self.grid[cardIndex][playerIndex] != 1:
                        self.grid[cardIndex][playerIndex] = 0
        
    def display(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                print("%8.2f" % (self.grid[i][j]), end='')
                
            print("\n")
            
    def displayPretty(self):
        print("Suspects: %d candidate(s) %s" % (self.numSuspectCandidates(), self.suspectCandidates()))
        for card in suspects:
            for playerName in clueUtils.playerNames:
                print("%8.2f" % (self.at(card, playerName)), end='')
                
            print("%8.2f\t%s\n" % (self.at(card, "mystery"), card))
        
        print("Weapons: %d candidate(s) %s" % (self.numWeaponCandidates(), self.weaponCandidates()))
        for card in weapons:
            for playerName in clueUtils.playerNames:
                print("%8.2f" % (self.at(card, playerName)), end='')
                
            print("%8.2f\t%s\n" % (self.at(card, "mystery"), card))
        
        print("Rooms: %d candidate(s) %s" % (self.numRoomCandidates(), self.roomCandidates()))
        for card in rooms:
            for playerName in clueUtils.playerNames:
                print("%8.2f" % (self.at(card, playerName)), end='')
                
            print("%8.2f\t%s\n" % (self.at(card, "mystery"), card))
    
    def suspectCandidates(self):
        candidates = []
        for card in clueUtils.suspects:
            cardIndex = clueUtils.allCards.index(card)
            if (self.grid[cardIndex][mysteryIndex] >= epsilon):
                candidates.append(card)
            
        return candidates
    
    def weaponCandidates(self):
        candidates = []
        for card in clueUtils.weapons:
            cardIndex = clueUtils.allCards.index(card)
            if (self.grid[cardIndex][mysteryIndex] >= epsilon):
                candidates.append(card)
        
        return candidates
    
    def roomCandidates(self):
        candidates = []
        for card in clueUtils.rooms:
            cardIndex = clueUtils.allCards.index(card)
            if (self.grid[cardIndex][mysteryIndex] >= epsilon):
                candidates.append(card)
            
        return candidates
    
    def numCandidates(self):
        numCandidates = 0
        for card in allCards:
            cardIndex = allCards.index(card)
            if (self.grid[cardIndex][mysteryIndex] >= epsilon):
                numCandidates = numCandidates + 1
            
        return numCandidates
    
    def numSuspectCandidates(self):
        numCandidates = 0
        for card in clueUtils.suspects:
            cardIndex = clueUtils.allCards.index(card)
            if (self.grid[cardIndex][mysteryIndex] >= epsilon):
                numCandidates = numCandidates + 1
            
        return numCandidates
    
    def numWeaponCandidates(self):
        numCandidates = 0
        for card in clueUtils.weapons:
            cardIndex = clueUtils.allCards.index(card)
            if (self.grid[cardIndex][mysteryIndex] >= epsilon):
                numCandidates = numCandidates + 1
                
        return numCandidates
    
    def numRoomCandidates(self):
        numCandidates = 0
        for card in clueUtils.rooms:
            cardIndex = clueUtils.allCards.index(card)
            if (self.grid[cardIndex][mysteryIndex] >= epsilon):
                numCandidates = numCandidates + 1
            
        return numCandidates
    
    def displayCandidates(self):
        for card in allCards:
            print("%8.2f %s\n" % (self.at(card,"mystery"), card))

#Test code
if __name__ == "__main__":
    myTestGrid = clueGrid()
    myTestGrid.display()
    myTestGrid.readGuessLog()
    loopCount = myTestGrid.updateCardProbabilities()
    print("Loop Count: %d" % (loopCount))
    myTestGrid.displayPretty()
#   print(clueUtils.numPlayerCards)
