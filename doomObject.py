import colored
from colored import stylize

def greenText(text):
    return stylize(text, colored.fg("green"))

class DoomObject():
    def __init__(self, json):
        self.id = json['id']
        self.x = json['position']['x']
        self.y = json['position']['y']
        self.z = json['position']['z']
        self.height = json['height']
        self.angle = json['angle']
        self.health = json['health']
        self.distanceFromPlayer = json['distance']
        self.type = json['type']
        
    def print(self):
        #print(greenText("PlayerId: " + str(self.id)))
        print(greenText("Id:" + str(self.id)))
        print("distance from me: " + str(self.distanceFromPlayer))
        print('''
        x: {0}, y: {1}, z: {2}
        height: {3}
        health: {4}
        angle: {5}
        type: {6}
        '''.format(self.x, self.y, self.z, self.height, self.health, self.angle, self.type))