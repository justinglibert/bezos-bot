import math
from policy import Policy


def getDistance(x1, y1, x2 ,y2):
        dis = math.sqrt((x1-x2)  ** 2 + (y1-y2) ** 2)
        return dis


#Default
polNothing = Policy(lambda world: 1, lambda world, agent: print("Nothing to do"))


#Dying
def polDeadUtility(world):
    print(world.getMe().health)
    return int(world.getMe().health <= 0) * 10**10

def polDeadExecute(world, agent):
    me = agent.api.getPlayerInfo()
    world.resetMe(me)
    agent.api.sendAction("shoot")
    print("Come back to life bezos")

polDead = Policy(polDeadUtility, polDeadExecute)


#Weapons
def polShotgunExecute(world, agent):
    closestChainsaw = world.findClosestObjectByType('Shotgun')
    agent.goTo(closestChainsaw.x, closestChainsaw.y)


polShotGun = Policy(lambda world: 500 *int(world.getMe().weapons['Shotgun'] == False), polShotgunExecute)


def polChainsawExecute(world, agent):
    closestChainsaw = world.findClosestObjectByType('Chainsaw')
    agent.goTo(closestChainsaw.x, closestChainsaw.y)

polChainsaw= Policy(lambda world: 200 *int(world.getMe().weapons['Chainsaw'] == False), polChainsawExecute)




def polShootPlayerUtility(world):
    closePlayers = world.rankPlayersByDistance()
    closest = closePlayers[0]
    me = world.getMe()
    return (getDistance(closest.x, closest.y, me.x, me.y) < 10000) * 300

def polShootPlayerExecute(world, agent):
    closePlayers = world.rankPlayersByDistance()
    me = world.getMe()
    closest = closePlayers[0]
    distance = getDistance(closest.x, closest.y, me.x, me.y)
    agent.goTo(closest.x, closest.y)
    if distance < 1000:
        agent.api.sendAction("shoot")
    

polShootPlayer = Policy(polShootPlayerUtility, polShootPlayerExecute)


Policies = [polNothing, polDead, polShotGun, polChainsaw, polShootPlayer]