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
    "angle": -90,
    "health": 100,
    "type": 1,
    "distance": 200
})

def angleToPos(obj, x, y):
    dis = math.sqrt((x-obj.x) ** 2 + (y-obj.y) ** 2)
    x_off = x - obj.x
    y_off = y - obj.y

    if (dis > 0 or dis < 0):
        if(y_off > 0):
            alpha = (math.acos(x_off / dis) * 180 / math.pi)
        else:
            alpha = -(math.acos(x_off / dis) * 180 / math.pi)
        print("alpha " + str(alpha))
    elif (dis == 0):
        return 0

    t = alpha - obj.angle

    
    return t


def findCoordinates(obj, angle, distance):
    alpha = (math.pi/180) * (obj.angle + angle)

    x = obj.x + distance * math.cos(alpha)

    y = obj.y + distance * math.sin(alpha)
    
    return int(round(x)), int(round(y))

print(angleToPos(testObj, -10, -10 ))
