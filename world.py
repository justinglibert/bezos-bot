from doomObject import DoomObject
from player import Player
import math 

BIG_DISTANCE = 1000000000000000000000000

def getDistance(x1, y1, x2 ,y2):
        dis = math.sqrt((x1-x2)  ** 2 + (y1-y2) ** 2)
        return dis



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


    def resetMe(self, me):
        self.playerId = me['id']
    
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


    def rankPlayersByDistance(self):
        players = list({x for x in self.players if x.me == False})
        me = self.getMe()   
        players = sorted(players, key= lambda p: getDistance(p.x, p.y, me.x, me.y))
        return players
        


    def findClosestObjectByType(self, type):
        objects = self.objects
        closest = None
        distance = BIG_DISTANCE

        for obj in objects:
            if obj.type == type:
                if obj.distanceFromPlayer < distance:
                    distance = obj.distanceFromPlayer
                    closest = obj
        
        return closest

    def print(self):
        for p in self.players:
            p.print()
        for o in self.objects:
            o.print()
        