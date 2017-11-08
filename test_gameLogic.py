#!/usr/bin/env python3

import unittest
import random
from gameLogic import *
from gameClass import GameState
from playerClass import Player

class UnitTestGameLogic(unittest.TestCase):

    def setUp(self):
        names = [str(x) for x in range(10)]
        players = []
        for i in names:
            players.append(Player(i))
        self.tester1 = None
        self.playersForTest = players


    def tearDown(self):
        pass

    def test_setUpMatch(self):
        for i in range(5, 11):
            self.tester1 = GameState(self.playersForTest[ : i])
            setUpMatch(self.tester1)
            self.tester1.setUpPolicyDeck()
            self.assertEqual(len(self.tester1.playerList), i)
            self.assertEqual(self.tester1.drawDeck.count("Liberal"), 6)
            self.assertEqual(self.tester1.drawDeck.count("Fascist"), 11)
            self.assertEqual(self.tester1.discardPile, [])
            self.assertEqual(self.tester1.policyList, [])
            self.assertEqual((self.tester1.president, self.tester1.chancellor, self.tester1.previousChancellor, self.tester1.previousPresident, self.tester1.prospectiveChancellor, self.tester1.electionTrack, self.tester1.availableBullets, self.tester1.vetoAvailable, self.tester1.peeked, self.tester1.selected, self.tester1.viewed),
                             (None, None, None, None, None, 0, 2, False, False, False, False))
            self.assertEqual(len(self.tester1.presidentList), 0)
            if i == 5:
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Liberal"]), 3)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Fascist"]), 1)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Hitler"]), 1)
            elif i == 6:
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Liberal"]), 4)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Fascist"]), 1)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Hitler"]), 1)
            elif i == 7:
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Liberal"]), 4)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Fascist"]), 2)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Hitler"]), 1)
            elif i == 8:
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Liberal"]), 5)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Fascist"]), 2)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Hitler"]), 1)
            elif i == 9:
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Liberal"]), 5)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Fascist"]), 3)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Hitler"]), 1)
            if i == 10:
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Liberal"]), 6)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Fascist"]), 3)
                self.assertEqual(len([x for x in self.tester1.playerList if x.role == "Hitler"]), 1)
        return

    def test_getSurvivingPlayerCount(self):
        self.tester1 = GameState(self.playersForTest)
        setUpMatch(self.tester1)
        self.assertEqual(len(self.tester1.playerList), 10)
        self.tester1.playerList[0].alive = False
        self.assertEqual(len(self.tester1.playerList), 10)
        self.assertEqual(getSurvivingPlayerCount(self.tester1), 9)
        self.tester1.playerList[1].alive = False
        self.assertEqual(len(self.tester1.playerList), 10)
        self.assertEqual(getSurvivingPlayerCount(self.tester1), 8)
        return

    def test_policyCounter(self):
        for _ in range(100):
            self.tester1 = GameState(self.playersForTest)
            setUpMatch(self.tester1)
            self.tester1.setUpPolicyDeck()
            for i in range(5):
                self.tester1.policyList.append(self.tester1.drawDeck.pop(0))
                self.tester1.discardPile.append(self.tester1.drawDeck.pop(0))
                self.tester1.discardPile.append(self.tester1.drawDeck.pop(0))
                self.assertEqual(len(self.tester1.policyList) + len(self.tester1.drawDeck) + len(self.tester1.discardPile), 17)
                self.assertEqual(self.tester1.policyList.count("Liberal") + self.tester1.drawDeck.count("Liberal") + self.tester1.discardPile.count("Liberal"), 6)
                self.assertEqual(self.tester1.policyList.count("Fascist") + self.tester1.drawDeck.count("Fascist") + self.tester1.discardPile.count("Fascist"), 11)
                self.assertEqual(policyCounter(self.tester1), ((6 - (self.tester1.drawDeck.count("Liberal") + self.tester1.discardPile.count("Liberal"))), (11 - (self.tester1.drawDeck.count("Fascist") + self.tester1.discardPile.count("Fascist")))))
        return

    def test_fascistElectionWin(self):
        self.tester1 = GameState(self.playersForTest)
        setUpMatch(self.tester1)
        self.tester1.setUpPolicyDeck()
        self.assertEqual(fascistElectionWin(self.tester1), None)
        self.tester1.policyList = ["Liberal", "Liberal", "Fascist"]
        self.assertEqual(fascistElectionWin(self.tester1), None)
        self.tester1.policyList += ["Liberal", "Liberal", "Fascist"]
        self.assertEqual(fascistElectionWin(self.tester1), None)
        self.tester1.policyList.append("Fascist")
        testPlayer = Player("Test")
        testPlayer.role = "Liberal"
        self.tester1.playerList.append(testPlayer)
        self.tester1.chancellor = "Test"
        self.assertEqual(self.tester1.policyList.count("Fascist"), 3)
        self.assertEqual(fascistElectionWin(self.tester1), False)
        self.tester1.playerList.pop()
        testPlayer.role = "Hitler"
        self.tester1.playerList.append(testPlayer)
        self.tester1.chancellor = "Test"
        self.assertEqual(fascistElectionWin(self.tester1), True)
        self.tester1.policyList += ["Fascist", "Fascist", "Fascist"]
        self.assertEqual(fascistElectionWin(self.tester1), True)
        return

    def test_fascistPolicyWin(self):
        self.tester1 = GameState(self.playersForTest)
        setUpMatch(self.tester1)
        self.tester1.setUpPolicyDeck()
        self.assertEqual(fascistPolicyWin(self.tester1), False)
        self.tester1.policyList += ["Liberal", "Liberal", "Fascist"]
        self.assertEqual(fascistPolicyWin(self.tester1), False)
        self.tester1.policyList += ["Fascist", "Fascist", "Fascist"]
        self.assertEqual(fascistPolicyWin(self.tester1), False)
        self.tester1.policyList += ["Liberal", "Fascist", "Fascist"]
        self.assertEqual(fascistPolicyWin(self.tester1), True)
        return

    def test_liberalPolicyWin(self):
        self.tester1 = GameState(self.playersForTest)
        setUpMatch(self.tester1)
        self.tester1.setUpPolicyDeck()
        self.assertEqual(liberalPolicyWin(self.tester1), False)
        self.tester1.policyList += ["Liberal", "Liberal", "Fascist"]
        self.assertEqual(liberalPolicyWin(self.tester1), False)
        self.tester1.policyList += ["Liberal", "Liberal", "Fascist"]
        self.assertEqual(liberalPolicyWin(self.tester1), False)
        self.tester1.policyList.append("Liberal")
        self.assertEqual(liberalPolicyWin(self.tester1), True)
        return

    def test_liberalFuckHitlerWin(self):
        test1 = Player('Test1')
        test2 = Player('Test2')
        test3 = Player("Test3")
        test1.role = "Hitler"
        test2.role = "Liberal"
        test3.role = "Fascist"
        self.assertEqual(liberalFuckHitlerWin(test1), True)
        self.assertEqual(liberalFuckHitlerWin(test2), False)
        self.assertEqual(liberalFuckHitlerWin(test3), False)
        return

    def test_electionTracker(self):
        for _ in range(20):
            seed = random.randint(0, 10)
            test1 = [("ja", "testName") for _ in range(seed)] + [("nein", "testName2") for _ in range(10 - seed)]
            self.assertEqual(electionTracker(test1), seed > 5)
        return

    def test_electedChancellor(self):
        self.tester1 = GameState(self.playersForTest)
        setUpMatch(self.tester1)
        self.tester1.setUpPolicyDeck()
        self.tester1.president = "Pres1"
        electedChancellor(self.tester1, "Chan1")
        self.assertEqual(self.tester1.president, "Pres1")
        self.assertEqual(self.tester1.previousPresident, "Pres1")
        self.assertEqual(self.tester1.chancellor, "Chan1")
        self.assertEqual(self.tester1.previousChancellor, "Chan1")
        self.tester1.president = "Pres2"
        self.tester1.prospectiveChancellor = "Chan2"
        self.assertEqual(self.tester1.president, "Pres2")
        self.assertEqual(self.tester1.previousPresident, "Pres1")
        self.assertEqual(self.tester1.chancellor, "Chan1")
        self.assertEqual(self.tester1.previousChancellor, "Chan1")
        electedChancellor(self.tester1, "Chan2")
        self.assertEqual(self.tester1.president, "Pres2")
        self.assertEqual(self.tester1.previousPresident, "Pres2")
        self.assertEqual(self.tester1.chancellor, "Chan2")
        self.assertEqual(self.tester1.previousChancellor, "Chan2")
        self.tester1.president = "Pres3"
        self.tester1.prospectiveChancellor = "Chan3"
        # election bid fails
        self.assertEqual(self.tester1.president, "Pres3")
        self.assertEqual(self.tester1.previousPresident, "Pres2")
        self.assertEqual(self.tester1.chancellor, "Chan2")
        self.assertEqual(self.tester1.previousChancellor, "Chan2")
        return

    def test_canBeChancellor(self):
        self.tester1 = GameState(self.playersForTest)
        setUpMatch(self.tester1)
        self.tester1.setUpPolicyDeck()
        self.tester1.president = "Pres2"
        self.tester1.previousPresident = "Pres1"
        self.tester1.previousChancellor = "Chan1"
        self.tester1.prospectiveChancellor = "Chan2"
        self.assertEqual(canBeChancellor(self.tester1, "Chan2"), True)
        electedChancellor(self.tester1, self.tester1.prospectiveChancellor)
        self.tester1.president = "Pres3"
        self.tester1.prospectiveChancellor = "Pres2"
        self.assertEqual(canBeChancellor(self.tester1, self.tester1.prospectiveChancellor), False)
        self.tester1.prospectiveChancellor = "Chan2"
        self.assertEqual(canBeChancellor(self.tester1, self.tester1.prospectiveChancellor), False)
        self.tester1.prospectiveChancellor = "Pres1"
        self.assertEqual(canBeChancellor(self.tester1, self.tester1.prospectiveChancellor), True)
        self.tester1.prospectiveChancellor = "Chan1"
        self.assertEqual(canBeChancellor(self.tester1, self.tester1.prospectiveChancellor), True)
        electedChancellor(self.tester1, self.tester1.prospectiveChancellor)
        self.tester1.president = "Pres4"
        self.tester1.prospectiveChancellor = "Pres3"
        self.assertEqual(canBeChancellor(self.tester1, self.tester1.prospectiveChancellor), False)
        self.tester1.prospectiveChancellor = "Chan1"
        self.assertEqual(canBeChancellor(self.tester1, self.tester1.prospectiveChancellor), False)
        self.tester1.prospectiveChancellor = "Pres2"
        self.assertEqual(canBeChancellor(self.tester1, self.tester1.prospectiveChancellor), True)
        self.tester1.prospectiveChancellor = "Chan2"
        self.assertEqual(canBeChancellor(self.tester1, self.tester1.prospectiveChancellor), True)        
        return

    def test_canVeto(self):
        self.tester1 = GameState(self.playersForTest)
        setUpMatch(self.tester1)
        self.tester1.setUpPolicyDeck()
        canVeto(self.tester1)
        self.assertEqual(self.tester1.vetoAvailable, False)
        self.tester1.policyList = ["Liberal", "Liberal", "Liberal", "Liberal", "Fascist"]
        canVeto(self.tester1)
        self.assertEqual(self.tester1.vetoAvailable, False)
        self.tester1.policyList = ["Liberal", "Liberal", "Liberal", "Liberal", "Liberal"]
        canVeto(self.tester1)
        self.assertEqual(self.tester1.vetoAvailable, False)     
        self.tester1.policyList = ["Liberal", "Liberal", "Fascist", "Fascist", "Fascist"]
        canVeto(self.tester1)
        self.assertEqual(self.tester1.vetoAvailable, False)
        self.tester1.policyList = ["Fascist", "Fascist", "Fascist", "Fascist", "Fascist"]
        canVeto(self.tester1)
        self.assertEqual(self.tester1.vetoAvailable, True)
        self.tester1.vetoAvailable = False
        self.tester1.policyList = ["Fascist", "Fascist", "Fascist", "Fascist", "Fascist", "Liberal"]
        canVeto(self.tester1)
        self.assertEqual(self.tester1.vetoAvailable, True)
        self.tester1.vetoAvailable = False
        self.tester1.policyList = ["Fascist", "Fascist", "Fascist", "Fascist", "Fascist", "Liberal", "Liberal"]
        canVeto(self.tester1)
        self.assertEqual(self.tester1.vetoAvailable, True)

    def test_policyHandling(self):
        pass

    def test_showPartyCard(self):
        pass

    def test_executePlayer(self):
        pass

    def test_electionSetup(self): 
        ''' Known potential bug. If a nomination bid fails, the former president is eligible to be elected chancellor in the next round.
        line 257 in gameLogic.py was inserted to assure that if an election fails, the previous president is stored as the current
        elected president rather than the recent failed president.'''
        pass

    def test_getVotes(self):
        pass

    def test_viewPartyAffilition(self):
        pass

    def test_policyPeek(self):
        pass

    def test_nextPresident(self):
        pass

    def test_selectNextPresident(self):
        pass

    def test_citizensFrustrated(self):
        pass


if __name__ == '__main__':
    unittest.main()