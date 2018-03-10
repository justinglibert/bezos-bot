from doomObject import DoomObject
from player import Player
class World():
    def __init__(self, me, objects, players):
        self.playerId = me['id']
        self.players = set()
        self.players.add(Player(me, True))
        for p in players:
            if p['type'] == 'Player' and p['id'] != self.playerId:
                self.players.add(Player(p))
        self.objects = set()
        for o in objects:
            if not o['type'] == 'Player':
                self.objects.add(DoomObject(o))


    def update(self, objects, players):
        self.updateObjects(objects)
        self.updatePlayers(players)


    def updatePlayers(self, players):
        self.players.clear()
        for p in players:
            if p['type'] == 'Player':
                if p['id'] == self.playerId:
                    self.players.add(Player(p, True))
                else:
                    self.players.add(Player(p))


    def updateObjects(self, objects):
        self.objects.clear()
        for o in objects:
            if not o['type'] == 'Player':
                self.objects.add(DoomObject(o))


    def getMe(self):
        mes = list({x for x in self.players if x.id == self.playerId})
        return mes[0]

    def printPlayers(self):
        players = sorted(self.players, key=lambda k: k.id) 
        for p in players:
            p.print()


    def printObjects(self):
        objects = sorted(self.objects, key=lambda k: k.id) 
        for o in objects:
            o.print()


    def print(self):
        for p in self.players:
            p.print()
        for o in self.objects:
            o.print()
        