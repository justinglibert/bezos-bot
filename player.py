import colored
from colored import stylize
import math
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
    
    def angleToPos(self, x, y):
        dis = math.sqrt((x-self.x) ** 2 + (y-self.y) ** 2)
        x_off = x - self.x

        y_off = y - self.y

        alpha = (math.acos(x_off / dis) * 180 / math.pi) 

        if (y_off > 0):
            return (alpha)
        else:
            return (360 - alpha) % 360
    
    def distanceToPos(self, x ,y):
        dis = math.sqrt((x-self.x) ** 2 + (y-self.y) ** 2)
        return dis
    
    def findCoordinates(self, angle, distance):
        alpha = (math.pi/180) * (self.angle + angle)
        x = self.x + distance * math.cos(alpha)
        y = self.y + distance * math.sin(alpha)
        
        return int(round(x)), int(round(y))