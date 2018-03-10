from api import Api
import colored
from colored import stylize
from doomObject import DoomObject
from player import Player
from world import World
from agent import Agent
import time
import os
from timer import RepeatedTimer
API_ENDPOINT = "http://192.168.43.222:6001/api"
api = Api(API_ENDPOINT)
#Hyperparameters
QUERY_OBJECT_FREQUENCY = 2
QUERY_PLAYER_FREQUENCY = 0.5
DISTANCE = 1000

def clearscreen(numlines=100):
  """Clear the console.
numlines is an optional argument used only as a fall-back.
"""

  if os.name == "posix":
    # Unix/Linux/MacOS/BSD/etc
    os.system('clear')
  elif os.name in ("nt", "dos", "ce"):
    # DOS/Windows
    os.system('CLS')
  else:
    # Fallback for other operating systems.
    print('\n' * numlines)



def queryObjects(world):
    objects = api.getObjects(DISTANCE)
    world.updateObjects(objects)

def queryPlayers(world, agent):
    players = api.getPlayers()
    world.updatePlayers(players)
    agent.updateMe(world.getMe())


def init():
    me = api.getPlayerInfo()
    players = api.getPlayers()
    objects = api.getObjects(DISTANCE)
    world = World(me, objects, players)
    world.getMe().print()
    agent = Agent(api, world.getMe())
    return world, agent

def main():
    #First init
    world, agent = init()
    queryObjectsTimer = RepeatedTimer(QUERY_OBJECT_FREQUENCY, queryObjects, world)
    queryPlayersTimer = RepeatedTimer(QUERY_PLAYER_FREQUENCY, queryPlayers, world, agent)

    while True:
        print(stylize("BEZOS BOT", colored.fg("green")))
        agent.print()
        #clearscreen()
        #world.printObjects()
        time.sleep( 1 / 60 * 3)

        

    #print(api.sendAction("shoot")) 
    #print(api.turn(200))
    #print(api.getObjects(1000))
if __name__ == "__main__":
    main()
