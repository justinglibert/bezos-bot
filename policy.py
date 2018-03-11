class Policy():
    def __init__(self, utility, actions):
        self.utility = utility
        self.actions = actions
    def execute(self, world, agent):
        self.actions(world, agent)
    def test(self, world, api = None):
        return self.utility(world)