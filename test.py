from object import DoomObject
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

def angleToPos(obj, x, y):
    dis = math.sqrt((x-obj.x) ** 2 + (y-obj.y) ** 2)
    x_off = x - obj.x
    y_off = y - obj.y

    if (dis > 0 or dis < 0):
        alpha = (math.acos(x_off / dis) * 180 / math.pi)
    elif (dis == 0):
        return 0

    if (y_off > 0):
        return (alpha)
    elif (y_off < 0):
        return (360 - alpha) % 360
    else:
        return 0


def findCoordinates(obj, angle, distance):
    alpha = (math.pi/180) * (obj.angle + angle)

    x = obj.x + distance * math.cos(alpha)

    y = obj.y + distance * math.sin(alpha)
    
    return int(round(x)), int(round(y))

print(findCoordinates(testObj, -90, 90 ))
