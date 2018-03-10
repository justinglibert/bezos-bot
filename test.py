from object import DoomObject
import unittest
import math

testObj = DoomObject ({
    "id": 1,
    'position': {
        "x": 100,
        "y": 100,
        "z": 0
    },
    "height": 1,
    "angle": 0,
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
    alpha = math.radians(self.angle + angle)
    x = self.x + distance * math.cos(alpha)
    y = self.y + distance * math.sin(alpha)
    return x, y


