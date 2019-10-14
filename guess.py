import clueUtils

class guess:
    
    def __init__(self, player, suspect, weapon, room):
        self.player = player
        self.suspect = suspect
        self.weapon = weapon
        self.room = room
        self.results = []
        self.revealed = "null"
        playerIndex = clueUtils.playerNames.index(player)
        for i in range(clueUtils.numPlayers):
            if i == playerIndex:
                self.results.append("guessed")
            else:
                self.results.append("null")
    
    @classmethod
    def fromFile(cls, filename) -> 'guess':
        guessList = []
        importListFromCSV(filename, guessList)
        return cls(player=guessList[0], suspect=guessList[1], weapon=guessList[2], room=guessList[3])
    
    def save(self, filename):
        guessList = [self.player, self.suspect, self.weapon, self.room]
        writeToFile(filename, guessList)
        
    def appendToGuessLog(self):
        guessList = [self.suspect, self.weapon, self.room]
        guessList = guessList + self.results
        print(guessList) #for debugging
        clueUtils.appendRowToFile("public/guessLog.csv", guessList)
        
    def display(self):
        print("%s's guess is %s with the %s in the %s" % (self.player, self.suspect, self.weapon, self.room))
    
    def cardList(self):
        list_of_guessed_cards = [self.suspect, self.weapon, self.room]
        return list_of_guessed_cards
    
    def inputResult(self, playerName, result):
        playerIndex = clueUtils.playerNames.index(playerName)
        if (result != "passed") and (result != "showed") and (result != "guessed"):
            print("Bad result \"%s\". Must be \"passed\" or \"showed\" or \"guessed\"." % (result))
        self.results[playerIndex] = result
    
    def input(self, playerName):
        #print("Enter player: ", end='')
        self.player = playerName
        while clueUtils.isPlayer(self.player) != True:
            print("Sorry, that is not a valid player.  Try again: ", end='')
            self.player = input()
        print("Enter suspect: ", end='')
        self.suspect = input()
        while clueUtils.isSuspect(self.suspect) != True:
            print("Sorry, that is not a valid suspect.  Try again: ", end='')
            self.suspect = input()
        print("Enter weapon: ", end='')
        self.weapon = input()
        while clueUtils.isWeapon(self.weapon) != True:
            print("Sorry, that is not a valid weapon.  Try again: ", end='')
            self.weapon = input()
        print("Enter room: ", end='')
        self.room = input()
        while clueUtils.isRoom(self.room) != True:
            print("Sorry, that is not a valid room.  Try again: ", end='')
            self.room = input()
        print("%s's guess is %s with the %s in the %s" % (self.player, self.suspect, self.weapon, self.room))