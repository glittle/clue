# clue.py
# Bill Skinner
# October 2019

import cluePlayer
import clueUtils

cluePlayers = []

for playerIndex in range(clueUtils.numPlayers):
    playerCards = []
    if clueUtils.playerTypes[playerIndex] != "human":
        clueUtils.importListFromCSV("cards/%s_cards.csv" % (clueUtils.playerNames[playerIndex]), playerCards)
    player = cluePlayer.cluePlayer(clueUtils.playerNames[playerIndex], playerCards, clueUtils.playerTypes[playerIndex])
    cluePlayers.append(player)

print("Welcome to Clue!")
print("This is a %d player game." % (clueUtils.numPlayers))
i = 1
for playerName in clueUtils.playerNames:
    print("Player %d: %s\t\t(%d cards)" % (i, playerName, clueUtils.numPlayerCards[i-1]))
    i = i + 1
print("Let's begin")

while True:
    print("Enter Player (Q to quit): ", end='')
    userInput = input()
    if (userInput == "Q") or (userInput == "q"):
        break
    while clueUtils.isPlayer(userInput) != True:
        print("Sorry, that is not a valid player.  Try again: ", end='')
        userInput = input()
    
    playerWhoGuessedIndex = clueUtils.playerNames.index(userInput)
    theGuess = cluePlayers[playerWhoGuessedIndex].playerGuess()
    playerIndex = playerWhoGuessedIndex + 1
    for i in range(clueUtils.numPlayers):
        if playerIndex >= clueUtils.numPlayers:
            playerIndex = 0
        if playerIndex != playerWhoGuessedIndex:
            theGuess = cluePlayers[playerIndex].checkHand(theGuess)
        if theGuess.results[playerIndex] == "showed":
            break
        playerIndex = playerIndex + 1
    theGuess.appendToGuessLog()
