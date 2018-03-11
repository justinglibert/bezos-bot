import requests
import json
from throttle import throttle
class Api():
    def __init__(self, endpoint):
        self.endpoint = endpoint
    def getPlayerInfo(self):
        r = requests.get( self.endpoint + '/player')
        return r.json()
    def getObjects(self, distance):
        payload = {'distance': distance}
        r = requests.get( self.endpoint + '/world/objects', params=payload)
        return r.json()
    def getObjectById(self, id):
        r = requests.get( self.endpoint + '/world/objects/' + id)
        return r.json()
    def getPlayers(self):
        r = requests.get( self.endpoint + '/players')
        return r.json()
    def getPlayerById(self, id):
        r = requests.get( self.endpoint + '/players/' + id)
        return r.json()
    def sendAction(self, action_type, amount = 10):
        payload = {'type': action_type, 'amount': amount}
        r = requests.post(self.endpoint + '/player/actions', data=json.dumps(payload))
        return r.text
    def turn(self, angle):
        payload = {'target_angle': angle}
        r = requests.post(self.endpoint + '/player/turn', data=json.dumps(payload))
        return r.text
    def moveTest(self, id, x , y):
        payload = {'id': id, 'x': x, 'y': y}
        r = requests.get( self.endpoint + '/world/movetest', params=payload)
        return r.json()['result']
    