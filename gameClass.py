import random

class GameState(object):
    """docstring for GameState"""
    def __init__(self, playerList):
        self.playerList = playerList
        self.drawDeck = []
        self.discardPile = []
        self.president = None
        self.chancellor = None
        self.previousChancellor = None
        self.previousPresident = None
        self.prospectiveChancellor = None
        self.electionTrack = 0
        self.availableBullets = 2
        self.policyList = []
        self.vetoAvailable = False
        self.presidentList = []
        self.peeked = False
        self.selected = False
        self.viewed = False
        
    def resetDeck(self):
        self.discardPile += self.drawDeck
        self.drawDeck = []
        random.shuffle(self.discardPile)
        self.drawDeck = self.discardPile
        self.discardPile = []
        return

    def setUpPolicyDeck(self):
        deck = []
        for _ in range(6):
            deck.append("Liberal")
        for _ in range(11):
            deck.append("Fascist")
        random.shuffle(deck)
        self.drawDeck = deck
        return

    def findPlayer(self, targetName):
        for player in self.playerList:
            if player.name == targetName:
                return player
        return