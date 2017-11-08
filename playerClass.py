class Player(object):
    """General Player Class. Fields: name, role. Methods: assignRole, clearRole
    playerShotorElected(returns True if player is Hitler to end game).""" 

    def __init__(self, name):
        self.name = name
        self.party = None
        self.role = None
        self.alive = None

    def assignRole(self, role):
        self.role = role
        if self.role == "Hitler":
            self.party = "Fascist"
        else:
            self.party = role
        self.alive = True
        return

    def clearRole(self):
        self.role = None

        return

    def playerShotOrElected(self):
        if self.role == "Hitler":
            return True
        return False

