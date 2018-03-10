import math

MOVE_FRAME = 40
INITIAL_FRESHNESS = 10
PERCEPTORS = 12
ANGLE_STEP = 10
PERCEPTORS_DISTANCE = 500
STRAFING = False

def distance(x1, y1, x2 ,y2):
        dis = math.sqrt((x1-x2)  ** 2 + (y1-y2) ** 2)
        return dis

class Agent():
    def __init__(self, api, me):
        self.api = api
        self.me = me
        self.goToCleared = None
        self.freshness = INITIAL_FRESHNESS
    def updateMe(self, me):
        self.me = me
    


    def findOffset(self):
        #Negative offset = to the left, positive = to the right
        #We start with the left ones (positive angles)
        for i in range(1, PERCEPTORS):
            print("Checking")
            angle = i * ANGLE_STEP
            x, y = self.me.findCoordinates(angle, PERCEPTORS_DISTANCE)
            clear = self.api.moveTest(self.me.id, x , y)
            if clear:
                #front_x, front_y = self.me.findCoordinates(0, PERCEPTORS_DISTANCE)
                #offset = distance(front_x, front_y, x, y)
                print("Found an angle offset: " + str(angle))
                return angle

        #Right ones
        for i in range(1, PERCEPTORS):
            print("Checking")
            angle = i * ANGLE_STEP
            x, y = self.me.findCoordinates(360 - angle, PERCEPTORS_DISTANCE)
            clear = self.api.moveTest(self.me.id, x , y)
            if clear:
                #front_x, front_y = self.me.findCoordinates(0, PERCEPTORS_DISTANCE)
                #offset = distance(front_x, front_y, x, y)
                print("Found an offset: " + str(-angle))
                return -angle
        
        print("No solutions found")
        return 0



    def goTo(self, x, y, noSlowDown = False):
        clear = self.goToCleared
        distance = self.me.distanceToPos(x, y)
        print(distance)
        speed = MOVE_FRAME
        if distance < 50:
            print("Done")
            return True


        #If clear has not be initialized we query the api
        if clear is None:   
            clear = self.api.moveTest(self.me.id, x, y)
            self.goToCleared = clear
            self.freshness = INITIAL_FRESHNESS
        #If it's not fresh or if it's false we query again
        elif self.freshness <= 0 or clear == False:
            clear = self.api.moveTest(self.me.id, x, y)
            self.goToCleared = clear
            self.freshness = INITIAL_FRESHNESS
        #Otherwise we decrease the freshness
        else:
            self.freshness = self.freshness - 1



        if clear:
            print("Clear")
            computedAngle = self.me.angleToPos(x, y)
            delta = self.me.angle - computedAngle
            #Slower approach when we get close
            if not noSlowDown:
                if distance < 1000:
                        speed = speed / 2

                if distance < 500:
                        speed = speed / 4

            if abs(delta) < 5:
                self.api.sendAction("forward", speed)
                return False
            else:
                self.api.turn(computedAngle)
                self.api.sendAction("forward", speed)
                return False
        else:
            print("Obstructed")
            angle = self.findOffset()
            if STRAFING:
                #Left to implement
                return False
            else:
                self.api.turn(angle + self.me.angle)
                self.api.sendAction("forward", speed)
            return False
    
    def print(self):
        self.me.print()