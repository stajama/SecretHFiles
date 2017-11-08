"""Main Game Logic and Controller."""

from gameClass import GameState
import random
import copy
import logging

# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s \
# - %(message)s')

rolesList = {5: ["Liberal", "Liberal", "Liberal", "Fascist", "Hitler"],  
             6: ["Liberal", "Liberal", "Liberal", "Liberal", "Fascist", "Hitler"],
             7: ["Liberal", "Liberal", "Liberal", "Liberal", "Fascist", "Fascist", "Hitler"],
             8: ["Liberal", "Liberal", "Liberal", "Liberal", "Liberal", "Fascist", "Fascist", "Hitler"],
             9: ["Liberal", "Liberal", "Liberal", "Liberal", "Liberal", "Fascist", "Fascist","Fascist", "Hitler"],
             10: ["Liberal", "Liberal", "Liberal", "Liberal", "Liberal", "Liberal", "Fascist", "Fascist","Fascist", "Hitler"]}

def setUpMatch(gameObject, roleDictionary=rolesList):
    roles = copy.copy(roleDictionary[len(gameObject.playerList)])
    random.shuffle(roles)
    for player in gameObject.playerList:
        player.assignRole(roles[-1])
        roles.pop()
    return

def getSurvivingPlayerCount(gameObject):
    counter = 0
    for player in gameObject.playerList:
        if player.alive:
            counter += 1
    return counter

def policyCounter(gameObject):
    logging.debug("in policyCounter(), policy list == " + str(gameObject.policyList))
    lCounter = 0
    fCounter = 0
    logging.debug("WTF is up with the policyList? " + str(gameObject) + ' ' + str(type(gameObject)))
    for policy in gameObject.policyList:
        if policy == "Liberal":
            lCounter += 1
        else:
            fCounter += 1
    return lCounter, fCounter

def fascistElectionWin(gameObject):
    if policyCounter(gameObject)[1] >= 3:
        newlyElectedChancellor = gameObject.findPlayer(gameObject.chancellor)
        return newlyElectedChancellor.playerShotOrElected()
    return

def fascistPolicyWin(gameObject):
    if policyCounter(gameObject)[1] >= 6:
        return True
    return False

def liberalPolicyWin(gameObject):
    if policyCounter(gameObject)[0] >= 5:
        return True
    return False

def liberalFuckHitlerWin(newlyAssassinatedPlayer):
    if newlyAssassinatedPlayer != None:
        return newlyAssassinatedPlayer.playerShotOrElected()
    return None

def electionTracker(voteList):
    ja = 0
    nein = 0
    print(voteList)
    for vote in voteList:
        if vote[0] == 'ja':
            ja += 1
        else:
            nein += 1
    logging.debug("Ja's and Nein's: " + str(ja) + " " + str(nein))
    return ja > nein

def electedChancellor(gameObject, playerName):
    gameObject.previousChancellor = playerName
    gameObject.chancellor = playerName
    if "*" in gameObject.president:
        gameObject.previousPresident = gameObject.president[: -1]
    else:
        gameObject.previousPresident = gameObject.president
    return

def canBeChancellor(gameObject, electedChancellor):
    currentPlayers = getSurvivingPlayerCount(gameObject)
    if currentPlayers <= 5:
        return electedChancellor != gameObject.previousChancellor and electedChancellor != gameObject.president and electedChancellor != gameObject.president + "*"
    else:
        return electedChancellor != gameObject.previousChancellor and electedChancellor != gameObject.previousPresident and electedChancellor != gameObject.president and electedChancellor != gameObject.president + "*"

def canVeto(gameObject):
    x = policyCounter(gameObject)[1]
    if x >= 5:
        gameObject.vetoAvailable = True
    return

def policyHandling(gameObject):
    # TODO - I think card selection is broken. Is supposed to discard non toPlay card and play toPlay.
    if len(gameObject.drawDeck) < 3:
        gameObject.resetDeck()
    logging.debug("policyHandling: showing drawDeck: " + str(gameObject.drawDeck))
    hand = gameObject.drawDeck[ : 3]
    logging.debug("policyHandling: showing hand after draw: " + str(hand))
    gameObject.drawDeck = gameObject.drawDeck[3 : ]
    logging.debug("policyHandling: showing drawDeck after hand drawn: " + str(gameObject.drawDeck))
    # Show to President.
    print(hand)
    while True:
        toDiscard = input("Choose 1 card to discard (1 - 3): ")
        try:
            toDiscard = int(toDiscard) - 1
        except ValueError:
            print("number must be a number 1, 2, or 3")
            continue
        if toDiscard >=0 and toDiscard <= 2:
            break
        else:
            print("number must be a number 1, 2, or 3")
    gameObject.discardPile.append(hand.pop(toDiscard))
    #Pass/show to Chancellor.
    print(hand)
    toPlay = None
    if gameObject.vetoAvailable:
        while True:
            toPlay = input("Select a policy card to play. You may veto these policies. : ")
            if toPlay.lower() == "veto":
                break
            else:
                try:
                    toPlay = int(toPlay) - 1
                except ValueError:
                    print("number must be a number 1 or 2. You may also enter 'veto' to veto current agendas.")
                    continue
                if toPlay == 0 or toPlay == 1:
                    break
                else:
                    print("number must be a number 1 or 2.")
        # to all
        if toPlay == "veto":
            # to all
            print("The Chancellor has chosen to veto the current set of agendas.")
            # to president
            choice = input("Will you allow the veto to stand?: ")
            if choice in "yes Yes Y y True yup Yup OK ok Ok ja yah yeah Ja Yah Yeah":
                # to all
                print("The President has accepted the veto motion and no policy was passed.")
                gameObject.discardPile += hand

            else:
                # to Chancellor
                print("The President has rejected your veto. Please select 1 of the 2 available policies to enact.")
                while True:
                    toPlay = input("You have no other option. 1 or 2: ")
                    try:
                        toPlay = int(toPlay) - 1
                    except ValueError:
                        print("number must be a number 1 or 2.")
                        continue
                    if toPlay == 0 or toPlay == 1:
                        break
                    else:
                        print("number must be a number 1 or 2.")
                        gameObject.policyList.append(hand[toPlay])
                        gameObject.discardPile.append(hand.pop())
        if toPlay.lower() == "veto":
            print("Current policy choices have been successfully vetoed.\n Election Tracker increases by 1.")
            gameObject.electionTrack += 1
        elif hand[toPlay] == "Liberal":
            print("A Liberal policy was enacted.")
            gameObject.policyList.append(hand[toPlay])
            gameObject.discardPile.append(hand.pop())
        else:
            print("A Fascist policy was enacted.")
            gameObject.policyList.append(hand[toPlay])
            gameObject.discardPile.append(hand.pop())
    else:
        while True:
            toPlay = input("Select a policy card to play. : ")
            try:
                toPlay = int(toPlay) - 1
            except ValueError:
                print("number must be a number 1 or 2.")
                continue
            if toPlay == 0 or toPlay == 1:
                break
            else:
                print("number must be a number 1 or 2.")
        if hand[toPlay] == "Liberal":
            print("A Liberal policy was enacted.")
        else:
            print("A Fascist policy was enacted.")
        gameObject.policyList.append(hand[toPlay])
        gameObject.discardPile.append(hand.pop())
    return
"""It's stupid to have a GameStatus object that tracks all game-state parameters, and them call parameters individually.
exp. policyHandlin() should accept gameObject. Only the fields within the object are being altered and it foolish to call them separately."""

def showPartyCard(gameObject, requestPlayer, showingPlayer):
    # to requestPlayer only
    outedPlayer = gameObject.findPlayer(showingPlayer)
    print(showingPlayer + " is a dirty " + outedPlayer.party + "!!!")
    return

def executePlayer(gameObject):
    # TODO = count and availableBullets need to be tested simultaneously. President cannot execute players after 2 have been killed.
    count = policyCounter(gameObject)[1]
    if count > 3:
        print("The President may now execute a player of their choice.")
        if gameObject.availableBullets > 0:
            # to president
            gameObject.availableBullets -= 1
            print("You may eliminate a player.")
            select = [(x, gameObject.playerList[x].name) for x in range(len(gameObject.playerList)) if gameObject.playerList[x].alive]
            while True:
                toKill = input("Select your target:\n" + str(select))
                try:
                    toKill = int(toKill)
                except ValueError:
                    print("enter a number corresponding to the selected execution victim.")
                    continue
                try:
                    gameObject.playerList[toKill].alive = False
                    # to all
                    print(gameObject.president + " has formally executed " + gameObject.playerList[toKill].name + ".")
                    return gameObject.playerList[toKill]

                except IndexError:
                    print("enter a number corresponding to the selected execution victim.")
    return

def electionSetup(gameObject):
    print(gameObject.president + " will now nominate a Chancellor.")
    success = None
    # to president
    while True:
        logging.debug('electionSetup check = ' + str(type(gameObject)) + ', ' + str(gameObject.playerList))
        while True:
            # pass # I believe this is erroneous.
            selection = input("Select a running mate. \n" + str([(x, gameObject.playerList[x].name) for x in range(len(gameObject.playerList)) if gameObject.playerList[x].alive]))
            try:
                selection = int(selection)
                break
            except:
                print("must enter number corresponding with nominated player.")
        if canBeChancellor(gameObject, gameObject.playerList[selection].name):
            print(gameObject.playerList[int(selection)].name + " has been nominated for Chancellor.")
            gameObject.prospectiveChancellor = gameObject.playerList[int(selection)].name
            if electionTracker(getVotes(gameObject)):
                electedChancellor(gameObject, gameObject.prospectiveChancellor)
                print("President " + gameObject.president + " and Chancellor " + gameObject.chancellor + " have been successfully elected.")
                success = True
                gameObject.electionTrack = 0
                break
            else:
                print("President " + gameObject.president + " and Chancellor " + gameObject.prospectiveChancellor + " have NOT been elected.")
                gameObject.president = gameObject.previousPresident
                gameObject.electionTrack += 1
                break
        else:
            print("This candidate can not be nominated.")
            continue
    citizensFrustrated(gameObject)
    return success

def getVotes(gameObject):
    #to all, secretly
    voteList = []
    print("Please submit your vote: Ja or Nein")
    for player in gameObject.playerList:
        if player.alive:
            voteList.append((input("Ja or Nein: ").lower(), player.name))
    return voteList
"""NOTE all int(inputString) calls will probably need to be adjusted. (+1)"""

def viewPartyAffiliation(gameObject):
    if policyCounter(gameObject)[1] == 2 and len(gameObject.playerList) >= 7 and not gameObject.viewed:
        gameObject.viewed = True
        # to all
        print("The President may now view the party affiliation card of another player.")
        while True:
            # to President only
            select = input("Choice a player: " + str([(x, gameObject.playerList[x].name) for x in range(len(gameObject.playerList)) if gameObject.playerList[x].alive]))
            try:
                select = int(select)
                showPartyCard(gameObject, gameObject.president, gameObject.playerList[select].name)
                break
            except (IndexError, ValueError):
                print("You must select the number corresponding to the player who's party membership card you would like to see.")
    return

def policyPeek(gameObject):
    if policyCounter(gameObject)[1] == 3 and len(gameObject.playerList) < 7 and not gameObject.peeked:
        gameObject.peeked = True
        # to all
        print("The President may now view the top 3 cards on the policy deck.")
        # to president only
        if len(gameObject.drawDeck) < 3:
            gameObject.resetDeck()
        peek = gameObject.drawDeck[ : 3]
        print(peek)
    return

def nextPresident(gameObject):
    logging.debug("gameObject should be type GameStatus: " + str(type(gameObject.presidentList[0])))
    if "*" not in gameObject.presidentList[0]:
        gameObject.previousPresident = gameObject.president
        gameObject.presidentList = gameObject.presidentList[1 : ] + [gameObject.presidentList[0]]
        gameObject.president = gameObject.presidentList[0]
    else:
        gameObject.previousPresident = gameObject.president
        gameObject.presidentList = gameObject.presidentList[1 : ]
        gameObject.president = gameObject.presidentList[0]
    return

def selectNextPresident(gameObject):
    if policyCounter(gameObject)[1] == 3 and len(gameObject.playerList) >= 7 and not gameObject.selected:
        gameObject.selected = True
        print("The President may now select the next Presidential Candidate.")
        # to president
        while True:
            select = input("Please select a candidate: "  + str([(x, gameObject.playerList[x].name) for x in range(0, len(gameObject.playerList)) if gameObject.playerList[x].alive]))
            try:
                select = int(select)
                logging.debug("in selectNextPresident: input should match -- " + str(select))
                print("President " + gameObject.president + " has selected " + gameObject.playerList[select].name + " to be the next Presidential Candidate.")
                gameObject.presidentList = [gameObject.presidentList[0]] + [gameObject.playerList[select].name + '*'] + gameObject.presidentList[1:]
                break
            except:
                print("You must select the number corresponding to the selected candidate.")
    return

def citizensFrustrated(gameObject):
    if gameObject.electionTrack >= 4:
        print("The people are unhappy and have forced a policy through.")
        forced = gameObject.drawDeck.pop(0)
        print('It was a ' + forced + " policy!")
        gameObject.policyList.append(forced)
        gameObject.electionTrack = 0
    return