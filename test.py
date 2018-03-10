from doomObject import DoomObject
import unittest
import math

testObj = DoomObject ({
    "id": 1,
    'position': {
        "x": 0,
        "y": 0,
        "z": 0
    },
    "height": 1,
    "angle": 180,
    "health": 100,
    "type": 1,
    "distance": 200
})

def angleToPos(self, x, y):
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


def findCoordinates(obj, angle, distance):
    alpha = (math.pi/180) * (obj.angle + angle)

    x = obj.x + distance * math.cos(alpha)

    y = obj.y + distance * math.sin(alpha)
    
    return int(round(x)), int(round(y))

print(angleToPos(testObj, 10, -10))
