import random
import guess
import clueUtils
import clueGrid

class cluePlayer:
    
    def __init__(self, name, cards, playerType):
        self.name = name
        self.cards = cards
        self.playerType = playerType
        self.myGrid = clueGrid.clueGrid()
        
        f = open("private/%s_saw.csv" % (self.name), 'a')
        for card in cards:
            f.write("\"%s\",\"%s\"\n" % (self.name, card))
        f.close()
        
    def display(self):
        print("Name: %s\n" % (self.name))
        print("Type: %s\n" % (self.playerType))
        print("Cards: %s\n" % (self.cards))
    
    def revealToHuman(self, theGuess):
        print("%s: I, %s, have %s" % (theGuess.playerName, self.name, theGuess.revealed)) 
        
    def revealToRandom(self, theGuess):
        f = open("private/%s_saw.csv" % (theGuess.playerName), 'a')
        f.write("\"%s\",\"%s\"\n" % (self.name, theGuess.revealed))
        f.close()
    
    def reveal(self, theGuess):
        playerIndex = clueUtils.playerNames.index(theGuess.playerName)
        playerType = clueUtils.playerTypes[playerIndex]
        if playerType == "human":
            self.revealToHuman(theGuess)
        elif playerType == "random":
            self.revealToRandom(theGuess)
        else:
            print("Unrecognized player type %s.  Revealing as if random." % (playerType))
            self.revealToRandom(theGuess)
    
    def humanCheckHand(self, theGuess):
        theGuessedCards = theGuess.cardList() 
        print("%s, check your hand. s = show, p = pass: " % (self.name), end='')
        userInput = input()
        while (userInput != "s") and (userInput != "p"):
            print("Invalid input. Enter \'s\' for show or \'p\' for pass: ", end='')
            userInput = input()
        if userInput == "s":
            theGuess.inputResult(self.name, "showed")
            print("Enter s for supect, w for weapon, or r for room: ", end='')
            userInput = input()
            while (userInput != "s") and (userInput != "w") and (userInput != "r"):
                print("Invalid input. Enter s for supect, w for weapon, or r for room: ", end='')
                userInput = input()
            if userInput == "s":
                theGuess.revealed = theGuessedCards[0]
            if userInput == "w":
                theGuess.revealed = theGuessedCards[1]
            if userInput == "r":
                theGuess.revealed = theGuessedCards[2]
            self.reveal(theGuess)
            return theGuess
        if userInput == "p":
            theGuess.inputResult(self.name, "passed")
            return theGuess
        
    def randomCheckHand(self, theGuess):
        theGuessedCards = theGuess.cardList() 
        for candidate in theGuessedCards:
            for card in self.cards:
                if candidate == card:
                    theGuess.inputResult(self.name, "showed")
                    theGuess.revealed = candidate
                    print("%s: Show" % (self.name))
                    self.reveal(theGuess)
                    return theGuess
            
        theGuess.inputResult(self.name, "passed")
        print("%s: Pass" % (self.name))
        return theGuess
        
    def checkHand(self, theGuess):
        if self.playerType == "human":
            return self.humanCheckHand(theGuess)
        if self.playerType == "random":
            return self.randomCheckHand(theGuess)
        else:
            print("Unknown player type %s. Using randomCheckHand." % (self.playerType))
            return self.randomCheckHand(theGuess)
        
    def requestUserToGuess(self):
        user_guess = guess.guess(self.name, "suspect", "weapon", "room")
        user_guess.input(self.name)
        return user_guess
        
    def generateRandomGuess(self):
        random_suspect = random.sample(clueUtils.suspects, 1)[0]
        random_weapon = random.sample(clueUtils.weapons, 1)[0]
        random_room = random.sample(clueUtils.rooms, 1)[0]
        random_guess = guess.guess(self.name, random_suspect, random_weapon, random_room)
        random_guess.display()
        return random_guess
    
    def generateSmartGuess(self):
        likelySuspects = self.myGrid.suspectCandidates()
        likelyWeapons = self.myGrid.weaponCandidates()
        likelyRooms = self.myGrid.roomCandidates()
        
#         print(likelySuspects)
#         print(likelyWeapons)
#         print(likelyRooms)
        
        guessSuspect = random.sample(likelySuspects, 1)[0]
        guessWeapon = random.sample(likelyWeapons, 1)[0]
        guessRoom = random.sample(likelyRooms, 1)[0]
        
        smartGuess = guess.guess(self.name, guessSuspect, guessWeapon, guessRoom)
        smartGuess.display()
        return smartGuess
    
    def playerGuess(self):
        if self.playerType == "human":
            theGuess = self.requestUserToGuess()
            return theGuess
        if self.playerType == "random":
            theGuess = self.generateSmartGuess()
            return theGuess
        print("Invalid player type")
    
    def makeAccusationIfKnown(self):
        self.updateLogic()
        if (self.myGrid.numCandidates() == 3):
            theSuspect = self.myGrid.suspectCandidates()[0]
            theWeapon = self.myGrid.weaponCandidates()[0]
            theRoom = self.myGrid.roomCandidates()[0]
            print("%s: My accusation is %s with the %s in the %s" % (self.name, theSuspect, theWeapon, theRoom))
    
    def updateLogic(self):
        self.myGrid.readGuessLog()
        self.myGrid.readPrivateLog("private/%s_saw.csv" % (self.name))
        self.myGrid.updateCardProbabilities()
    
#Test code
if __name__ == "__main__":
    cluePlayers = []

    for playerIndex in range(clueUtils.numPlayers):
        playerCards = []
        if clueUtils.playerTypes[playerIndex] != "human":
            clueUtils.importListFromCSV("cards/%s_cards.csv" % (clueUtils.playerNames[playerIndex]), playerCards)
        player = cluePlayer(clueUtils.playerNames[playerIndex], playerCards, clueUtils.playerTypes[playerIndex])
        cluePlayers.append(player)
    
    cluePlayers[0].myGrid.readGuessLog()
    cluePlayers[0].myGrid.readPrivateLog("private/%s_saw.csv" % (cluePlayers[0].name))
    cluePlayers[0].myGrid.updateCardProbabilities()

    cluePlayers[1].myGrid.readGuessLog()
    cluePlayers[1].myGrid.readPrivateLog("private/%s_saw.csv" % (cluePlayers[1].name))
    cluePlayers[1].myGrid.updateCardProbabilities()
    
    print("Player 1")
    cluePlayers[0].myGrid.displayPretty()
    
    print("Player 2")
    cluePlayers[1].myGrid.displayPretty()

#   print("%d" % (cluePlayers[1].myGrid.grid[8][6])) # Revolver, should be 0.00