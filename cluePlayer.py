import random
import guess
import clueUtils
import clueGrid

class cluePlayer:
    
    def __init__(self, name, cards, playerType):
        self.name = name
        self.cards = cards
        self.playerType = playerType
        self.grid = clueGrid.clueGrid()
        
    def display(self):
        print("Name: %s\n" % (self.name))
        print("Type: %s\n" % (self.playerType))
        print("Cards: %s\n" % (self.cards))
    
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
                    print("%s: I have %s" % (self.name, card))
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
    
    def playerGuess(self):
        if self.playerType == "human":
            theGuess = self.requestUserToGuess()
            return theGuess
        if self.playerType == "random":
            theGuess = self.generateRandomGuess()
            return theGuess
        print("Invalid player type")
        