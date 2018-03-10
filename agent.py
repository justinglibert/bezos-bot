MOVE_FRAME = 40
INITIAL_FRESHNESS = 5

class Agent():
    def __init__(self, api, me):
        self.api = api
        self.me = me
        self.goToCleared = None
        self.freshness = INITIAL_FRESHNESS
    def updateMe(self, me):
        self.me = me
    
    def goTo(self, x, y):
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
            return False
    
    def print(self):
        self.me.print()