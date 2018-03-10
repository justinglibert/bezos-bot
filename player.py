import colored
from colored import stylize

def greenText(text):
    return stylize(text, colored.fg("green"))

class Player():
    def __init__(self, json, me = False):
        self.me = me
        self.id = json['id']
        self.x = json['position']['x']
        self.y = json['position']['y']
        self.z = json['position']['z']
        self.height = json['height']
        self.angle = json['angle']
        self.health = json['health']

        self.type = 'Player'
        
    def print(self):
        #print(greenText("PlayerId: " + str(self.id)))
        print(greenText("PlayerId:" + str(self.id)))
        if self.me:
            print(greenText("This is me"))
        print('''
        x: {0}, y: {1}, z: {2}
        height: {3}
        health: {4}
        angle: {5}
        '''.format(self.x, self.y, self.z, self.height, self.health, self.angle))