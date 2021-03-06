import math
import colored
from colored import stylize
MOVE_FRAME = 50
INITIAL_FRESHNESS = 5
PERCEPTORS = 12
ANGLE_STEP = 15
PERCEPTORS_DISTANCE = 500
MULTIPLIER_TURN = 0.28
MULTIPLIER_CONSTANT = 5
STRAFING_COEF = 0.01
STRAFING = False


def greenText(text):
    return stylize(text, colored.fg("green"))

def getDistance(x1, y1, x2 ,y2):
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
    
    def setFreshness(self, freshness):
        self.freshness = freshness

    def findOffset(self):
        #Negative offset = to the left, positive = to the right
        #We start with the left ones (positive angles)
        x, y = self.me.findCoordinates(0, PERCEPTORS_DISTANCE)
        clear = self.api.moveTest(self.me.id, x , y)
        if clear:
                #front_x, front_y = self.me.findCoordinates(0, PERCEPTORS_DISTANCE)
                #offset = distance(front_x, front_y, x, y)
                print("Found an angle offset: " + str(0))
                return 0
        
        for i in range(1, PERCEPTORS):
            print("Checking")
            angle = i * ANGLE_STEP
            x, y = self.me.findCoordinates(angle, PERCEPTORS_DISTANCE)
            print("My Id according to agent" + str(self.me.id))
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


    def face(self, x, y):
        computedAngle = self.me.angleToPos(x, y)

        print("ComputedAngle: " + str(computedAngle)) 
        if abs(computedAngle) < 5:
            return True
        else:
            turn_type = None
            if computedAngle > 180:
                computedAngle = computedAngle - 360
            if computedAngle < -180:
                computedAngle = 360 + computedAngle
            if computedAngle > 0:
                turn_type = "turn-left"
            else:
                turn_type = "turn-right"
            self.api.sendAction(turn_type, abs(computedAngle) * MULTIPLIER_TURN + MULTIPLIER_CONSTANT)
            return False
    def goTo(self, x, y, noSlowDown = False):
        freshness = self.freshness
        print("RECTANGLE: " + str(greenText(self.me.isInRectangle())))
        if(not self.me.isInRectangle()):
            print("Not in rectangle")
            freshness = 0
        clear = self.goToCleared
        distance = self.me.distanceToPos(x, y)
        print("Going to: " + str(x) + " " + str(y))
        print("Angle: " + str(self.me.angleToPos(x, y)))
        print("Distance to objective:" + str(distance))
        speed = MOVE_FRAME
        if distance < 50:
            print("Done")
            return True

        #If it's not fresh or if it's false we query again
       
        elif freshness <= 0 or clear == False:
            print("RECHECKING THE CLARITY")
            if(self.api.moveTest(self.me.id, x, y)):
                clear = True
            elif(self.me.distanceToPos(x ,y) < PERCEPTORS_DISTANCE):
                clear = self.api.moveTest(self.me.id, x, y)
            else:
                x_close, y_close = self.me.findCoordinates(0, PERCEPTORS_DISTANCE)
                print("Coordinates to check: ", x_close, y_close)
                clear = self.api.moveTest(self.me.id, x_close, y_close)
            print("Clear: " + str(clear))
            self.goToCleared = clear
            self.freshness = INITIAL_FRESHNESS
        #Otherwise  we decrease the freshness
        else:
            self.freshness = self.freshness - 1



        if clear:
            print("Clear")
            computedAngle = self.me.angleToPos(x, y)
            #Slower approach when we get close
            if not noSlowDown:
                if distance < 1000:
                        speed = speed / 1.5

                if distance < 500:
                        speed = speed / 1.5
            print("ComputedAngle: " + str(computedAngle)) 

            if abs(computedAngle) < 5:
                self.api.sendAction("forward", speed)
                return False
            else:
                turn_type = None
                if computedAngle > 180:
                    computedAngle = computedAngle - 360
                if computedAngle < -180:
                    computedAngle = 360 + computedAngle
                if computedAngle > 0:
                    turn_type = "turn-left"
                else:
                    turn_type = "turn-right"
                self.api.sendAction(turn_type, abs(computedAngle) * MULTIPLIER_TURN + MULTIPLIER_CONSTANT)
                self.api.sendAction("forward", speed)
                return False
        else:
            print("Obstructed")
            computedAngle = self.findOffset()
            if STRAFING:
                #Left to implement
                return False
            else:
                turn_type = None
                if computedAngle > 180:
                    computedAngle = 360 - computedAngle
                if computedAngle < -180:
                    computedAngle = 360 + computedAngle
                if computedAngle > 0:
                    turn_type = "turn-left"
                else:
                    turn_type = "turn-right"
                self.api.sendAction(turn_type, abs(computedAngle) * MULTIPLIER_TURN + MULTIPLIER_CONSTANT)
                self.api.sendAction("forward", speed + 40)
            return False
    
    
    def goToBackward(self, x, y, x_facing, y_facing):
        ''' freshness = self.freshness
        clear = self.goToCleared

        if freshness <= 0 or clear == False:
            print("RECHECKING THE CLARITY")
            if(self.api.moveTest(self.me.id, x, y)):
                clear = True
            elif(self.me.distanceToPos(x ,y) < PERCEPTORS_DISTANCE):
                clear = self.api.moveTest(self.me.id, x, y)
            else:
                x_close, y_close = self.me.findCoordinates(0, PERCEPTORS_DISTANCE)
                print("Coordinates to check: ", x_close, y_close)
                clear = self.api.moveTest(self.me.id, x_close, y_close)
            print("Clear: " + str(clear))
            self.goToCleared = clear
            self.freshness = INITIAL_FRESHNESS
        #Otherwise  we decrease the freshness
        else:
            self.freshness = self.freshness - 1
            

        speed = MOVE_FRAME
        if not clear:
            computedAngle = self.findOffset()
            turn_type = None
            if computedAngle > 180:
                computedAngle = 360 - computedAngle
            if computedAngle < -180:
                computedAngle = 360 + computedAngle
            if computedAngle > 0:
                turn_type = "turn-left"
            else:
                turn_type = "turn-right"
            self.api.sendAction(turn_type, abs(computedAngle) * MULTIPLIER_TURN + MULTIPLIER_CONSTANT)
            self.api.sendAction("forward", speed + 40) '''


        computedAngle = self.me.angleToPos(x_facing, y_facing)
        distance = getDistance(self.me.x, self.me.y, x, y)
        print("ComputedAngle: " + str(computedAngle)) 
        if abs(computedAngle) >= 5:
            turn_type = None
            if computedAngle > 180:
                computedAngle = computedAngle - 360
            if computedAngle < -180:
                computedAngle = 360 + computedAngle
            if computedAngle > 0:
                turn_type = "turn-left"
            else:
                turn_type = "turn-right"
            self.api.sendAction(turn_type, abs(computedAngle) * MULTIPLIER_TURN + MULTIPLIER_CONSTANT)

        speed = MOVE_FRAME
        print("Distance backward: " + str(distance))
        if(distance > 700):
            strafe = self.me.getDistanceFromLines(x, y)
            if strafe <=  50:
                self.api.sendAction('strafe-left', 20 + abs(strafe) * STRAFING_COEF)
            elif strafe >= 50:
                self.api.sendAction('strafe-right', 20 + abs(strafe) * STRAFING_COEF)
            #Go Backward
            self.api.sendAction('backward', speed)
        elif distance > 50:
            speed = speed / 2
            #Get the correct strafe
            strafe = self.me.getDistanceFromLines(x, y) 
            if strafe <=  50:
                self.api.sendAction('strafe-left', 20 + abs(strafe) * STRAFING_COEF)
            elif strafe >= 50:
                self.api.sendAction('strafe-right', 20 + abs(strafe) * STRAFING_COEF)
            #Go Backward
            self.api.sendAction('backward', speed)
        else:
            return
            
    
    
    def print(self):
        self.me.print()