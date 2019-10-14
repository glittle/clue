# clueSetup.py

import csv
import random
import clueUtils

suspects = clueUtils.suspects
weapons = clueUtils.weapons
rooms = clueUtils.rooms
playerNames = clueUtils.playerNames
playerTypes = clueUtils.playerTypes
numPlayers = clueUtils.numPlayers

shuffledSuspects = random.sample(suspects, 6)
shuffledWeapons = random.sample(weapons, 6)
shuffledRooms = random.sample(rooms, 9)

theSuspect = shuffledSuspects[0]
theWeapon = shuffledWeapons[0]
theRoom = shuffledRooms[0]
solution = [theSuspect, theWeapon, theRoom]

remainingSuspects = shuffledSuspects[1:6]
remainingWeapons = shuffledWeapons[1:6]
remainingRooms = shuffledRooms[1:9]

remainingCards = remainingSuspects + remainingWeapons + remainingRooms
shuffledRemainingCards = random.sample(remainingCards, 18)

playerCards = []
for playerIndex in range(numPlayers):
    cards = []
    playerCards.append(cards)
        
cardIndex = 0
while cardIndex < 18:
    playerIndex = 0
    while playerIndex < numPlayers:
        if cardIndex >= 18:
            break
        playerCards[playerIndex].append(shuffledRemainingCards[cardIndex])
        cardIndex = cardIndex + 1
        playerIndex = playerIndex + 1

    
clueUtils.writeToFile("cards/mystery.csv", solution)
for i in range(numPlayers):
    clueUtils.writeToFile("cards/%s_cards.csv" % (playerNames[i]), playerCards[i])

print("Cards written to files")
