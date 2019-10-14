import csv

def importListFromCSV(filename, dest):
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            dest.append(row[0])

def importTwoListsFromCSV(filename, dest1, dest2):
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            dest1.append(row[0])
            dest2.append(row[1])

def writeToFile(filename, cards):
    f = open(filename, 'w')
    for card in cards:
        f.write("\"%s\"\n" % (card))
    f.close()
    
def appendRowToFile(filename, myList):
    f = open(filename, 'a')
    for i in range(len(myList)):
        if i < (len(myList) - 1):
            f.write("\"%s\"," % (myList[i]))
        else:
            f.write("\"%s\"\n" % (myList[i])) #last element in row
    f.close()

def isPlayer(userInput):
    for player in playerNames:
        if userInput == player:
            return(True)
    return(False)

def isSuspect(userInput):
    for suspect in suspects:
        if userInput == suspect:
            return(True)
    return(False)
        
def isWeapon(userInput):
    for weapon in weapons:
        if userInput == weapon:
            return(True)
    return(False)
        
def isRoom(userInput):
    for room in rooms:
        if userInput == room:
            return(True)
    return(False)

suspects = []
weapons = []
rooms = []
playerNames = []
playerTypes = []
numPlayerCards = []

importListFromCSV("setup/suspects.csv", suspects)
importListFromCSV("setup/weapons.csv", weapons)
importListFromCSV("setup/rooms.csv", rooms)
importTwoListsFromCSV("setup/playerNames.csv", playerNames, playerTypes)

numPlayers = len(playerNames)
numSuspects = len(suspects)
numWeapons = len(weapons)
numRooms = len(rooms)
allCards = suspects + weapons + rooms
numCards = len(allCards)

for i in range(numPlayers):
    initialNumCards = 0
    numPlayerCards.append(initialNumCards)

cardIndex = 0
while cardIndex < 18:
    playerIndex = 0
    while playerIndex < numPlayers:
        if cardIndex >= 18:
            break
        numPlayerCards[playerIndex] = numPlayerCards[playerIndex] + 1
        cardIndex = cardIndex + 1
        playerIndex = playerIndex + 1

#empty guessLog.csv file
file = open("public/guessLog.csv", 'w')
file.close()

#write header to guessLog.csv file
guessLogHeader = ["Suspect", "Weapon", "Room"]
for playerName in playerNames:
    guessLogHeader.append(playerName)
appendRowToFile("public/guessLog.csv", guessLogHeader)
