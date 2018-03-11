class Policy():
    def __init__(self, utility, actions, name):
        self.utility = utility
        self.actions = actions
        self.name = name
    def getName(self):
        return self.name
    def execute(self, world, agent):
        self.actions(world, agent)
    def test(self, world, api = None):
        return self.utility(world)