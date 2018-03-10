MOVE_FRAME = 10

class Agent():
    def __init__(self, api, me):
        self.api = api
        self.me = me
    def updateMe(self, me):
        self.me = me
    
    def goTo(self, x, y):
        clear = self.api.moveTest(self.me.id, x, y)
        if clear:
            self.api.sendAction("forward", MOVE_FRAME)
        else:
            print("Obstructed")
    
    def print(self):
        self.me.print()