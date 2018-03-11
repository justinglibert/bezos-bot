from doomObject import DoomObject
import unittest
import math

testObj = DoomObject ({
    "id": 1,
    'position': {
        "x": 10,
        "y": 10,
        "z": 0
    },
    "height": 1,
    "angle": 0,
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
    print ("alpha: " + str(alpha))

    angleToTurn = (alpha - obj.angle) % 360
    print("angleToTurn: " + str(angleToTurn))

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

print("Answer: " + str(angleToPos(testObj, -10, -10 )))
