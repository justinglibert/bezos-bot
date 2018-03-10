import colored
import math
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

    def angleToPos(self, x, y):
        dis = math.sqrt((x-self.x) ** 2 + (y-self.y) ** 2)
        x_off = x - self.x
        y_off = y - self.y

        if (dis > 0 or dis < 0):
            alpha = (math.acos(x_off / dis) * 180 / math.pi)
        elif (dis == 0):
            return 0

        if (y_off > 0):
            return (alpha)
        else:
            return (360 - alpha) % 360

    def findCoordinates(self, angle, distance):
        alpha = (math.pi/180) * (self.angle + angle)
        x = self.x + distance * math.cos(alpha)
        y = self.y + distance * math.sin(alpha)
        
        return int(round(x)), int(round(y))
    

