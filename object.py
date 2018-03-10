import colored
from colored import stylize

def printGreen(text):
    print(stylize(text, colored.fg("green")))

class DoomObject():
    def __init__(self, json):
        self.id = json['id']
        self.x = json['position']['x']
        self.y = json['position']['y']
        self.z = json['position']['z']
        self.height = json['height']
        self.angle = json['angle']
        self.health = json['health']
        self.type = json['type']
        self.distanceFromPlayer = json['distance']
    def __str__(self):
        return