#!/usr/bin/env python3

from playerClass import Player
from gameClass import GameState
from gameLogic import *
import random
import logging
import sys

runtimeInfo = sys.argv
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s \
- %(message)s')

if "debug" not in runtimeInfo:
    logging.disable(logging.DEBUG)



numOfPlayers = input("Number of Players: ")
try:
   numOfPlayers = int(numOfPlayers) 
except Exception as e:
    raise TypeError("Numbers only, closing...")
if numOfPlayers < 5:
    raise ValueError("Need more players. Time to make some friends, I guess...")
elif numOfPlayers > 10:
    raise ValueError("Too many players. Somebodies going to have to sit one out...")


def testFauxPlayerSetup(numberOfPlayers):
    playerList = ["Ricky", "Sara", "Randall", "Tod", "Joyce", "Rebecca", "Abigail", "Jim", "Tom", "Gloria"]
    random.shuffle(playerList)
    logging.debug("Set up fake players list " + str(playerList))
    hold = playerList[ : numberOfPlayers]
    return hold

def clearRoles(listOfPlayers):
    for player in listOfPlayers:
        player.clearRole()
    return

# Finalize Setup

# FOR TESTING
if "test" in runtimeInfo:
    playerList = testFauxPlayerSetup(numOfPlayers)
    playerList = [Player(x) for x in playerList]
else:
    playerList = []
    for i in range(1, numOfPlayers + 1):
        playerList.append(Player(input(str(i) + "th Player Name?: ")))

clearRoles(playerList)

keepPlaying = True
print("-" * 79)
while keepPlaying:
    game = GameState(playerList)
    logging.debug("game variable: type-" + str(type(game)))
    logging.debug("game playerList" + str(game.playerList))
    print(str([(x, game.playerList[x].name) for x in range(len(game.playerList))]))
    start = input("Whose up first?: ")
    try:
        start = int(start) - 1
    except:
        print("Bad input, closing...")
        break
    orderList = []
    for i in range(len(game.playerList)):
        orderList.append(game.playerList[i % len(game.playerList)].name)
    orderList = orderList[start: ] + orderList[ :start]
    logging.debug("Compare playerList: " + str([x.name for x in playerList]) + " ---- to orderList: " + str(orderList))
    game.presidentList = orderList
    setUpMatch(game)
    # for testing
    for player in game.playerList:
        print(player.name, player.party, player.role, player.alive)
    game.setUpPolicyDeck()
    while True:
        logging.debug("Showing policyCounter(): " + str(policyCounter(game)) + ' ' + str(type(policyCounter(game))))
        nextPresident(game)
        if electionSetup(game) != None:
            if fascistElectionWin(game):
                print('Fascists Win')
                break
            policyHandling(game)
            if fascistPolicyWin(game):
                print('Fascists Win')
                break
            elif liberalPolicyWin(game):
                print('Liberals Win')
                break
            policyPeek(game)
            viewPartyAffiliation(game)
            selectNextPresident(game)
            if liberalFuckHitlerWin(executePlayer(game)):
                print('Liberals Win')
                break
    for player in game.playerList:
        print(player.name, player.party, player.role, player.alive)
    continuePlay = input("another round?: ")
    if continuePlay in "No no n N NO gawd, please stop":
        keepPlaying = False

# if __name__ == '__main__':
#     main()
