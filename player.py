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
        self.currentWeapon = json['weapon']
        self.weapons = json['weapons']
        self.ammo = json['ammo']
        self.armor = json['armor']
        self.height = json['height']
        self.angle = json['angle']
        self.health = json['health']

        self.type = 'Player'


    def setCurrentWeapon(self, id):
        self.currentWeapon = id
        
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
    
    def oldAngleToPos(self, x, y):
        dis = math.sqrt((x-self.x) ** 2 + (y-self.y) ** 2)
        x_off = x - self.x
        y_off = y - self.y

        if (dis > 0 or dis < 0):
            if(y_off > 0):
                alpha = (math.acos(x_off / dis) * 180 / math.pi)
            else:
                alpha = -(math.acos(x_off / dis) * 180 / math.pi)
        elif (dis == 0):
            return 0

        t = alpha - self.angle
        if (t < -180):
            return round(360 + t) % 360
        elif( t > 180):
            return round(-360 + t) % 360
        else:
            return round(t)
    def angleToPos(self, x ,y):
        dx = x - self.x
        dy = y - self.y
        dis = math.sqrt(dx*dx + dy*dy)
        if (dis == 0):
            return 0
        # 180 < alpha < 0 -> angle between x=0 and position (x,y)
        if (dy > 0):
            alpha = math.acos(dx / dis) * 180 / math.pi
        else:
            alpha = - math.acos(dx / dis) * 180 / math.pi
        print ("alpha: " + str(alpha))

        angleToTurn = (alpha - self.angle) % 360
        print("angleToTurn: " + str(angleToTurn))

        if (angleToTurn > 180):
            result =  angleToTurn - 360
        elif (angleToTurn < -180):
            result = 360 + angleToTurn
        else:
            result = angleToTurn

        return result
    
    def distanceToPos(self, x ,y):
        dis = math.sqrt((x-self.x) ** 2 + (y-self.y) ** 2)
        return dis
    
    def findCoordinates(self, angle, distance):
        alpha = (math.pi/180) * (self.angle + angle)
        x = self.x + distance * math.cos(alpha)
        y = self.y + distance * math.sin(alpha)
        
        return int(round(x)), int(round(y))

    def isInRectangle(self):
        topX = 1700
        topY = 2276
        bottomX = -4175
        bottomY = -3615
        return (self.x >= bottomX and self.x <= topX and self.y >= bottomY and self.y <= topY)
    def getDistanceFromLines(self, x1, y1):
        if self.angle == 0:
            return self.x - x1
        elif self.angle == 180:
            return x1 - self.x
        a = math.tan((math.pi/180) * self.angle )
        b = -1
        c = y1 - a * x1
        print("a: " + str(a))
        if a == 0:
            return None
        else:
            dist = a * self.x + b * self.y + c / math.sqrt(a*a + b*b)
        if self.angle < 180:
            return dist
        else:
            return -dist        