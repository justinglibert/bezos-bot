from doomObject import DoomObject
import unittest
import math
import numpy.linalg

testObj = DoomObject ({
    "id": 1,
    'position': {
        "x": 3,
        "y": 0,
        "z": 0
    },
    "height": 1,
    "angle": 45,
    "health": 100,
    "type": 1,
    "distance": 200
})

def angleToPos(obj, x, y):
    dx = x - obj.x
    dy = y - obj.y
    dis = math.sqrt(dx*dx + dy*dy)
    if (dis == 0):
        return 0
    # 180 < alpha < 0 -> angle between x=0 and position (x,y)
    if (dy > 0):
        alpha = math.acos(dx / dis) * 180 / math.pi
    else:
        alpha = - math.acos(dx / dis) * 180 / math.pi

    angleToTurn = (alpha - obj.angle) % 360

    if (angleToTurn > 180):
        result =  angleToTurn - 360
    elif (angleToTurn < -180):
        result = 360 + angleToTurn
    else:
        result = angleToTurn

    return result

def findCoordinates(obj, angle, distance):
    alpha = (math.pi/180) * (obj.angle + angle)
    x = obj.x + distance * math.cos(alpha)
    y = obj.y + distance * math.sin(alpha)
    return int(round(x)), int(round(y))


# dist < 0 = go to the left, dist > 0 = go to the right
def getDistance(obj, x1, y1):
    if obj.angle == 0:
        return obj.x - x1
    elif obj.angle == 180:
        return x1 - obj.x
    a = math.tan((math.pi/180) * obj.angle )
    b = -1
    c = y1 - a * x1
    print("a: " + str(a))
    if a == 0:
        return None
    else:
        dist = a * obj.x + b * obj.y + c / math.sqrt(a*a + b*b)
    if obj.angle < 180:
        return dist
    else:
        return -dist
