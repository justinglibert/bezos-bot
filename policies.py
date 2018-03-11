import math
import time
from time import sleep
from policy import Policy






WEAPONS = {
    'Chainsaw': {
        'name': 'Chainsaw',
        'id': 8,
        'ammo': 'Bullets',
        'strength': 0
    },
    'Handgun': {
        'name': 'Handgun',
        'id': 2,
        'ammo': 'Bullets',
        'strength': 1
    },
    'Shotgun': {
        'name': 'Shotgun',
        'id': 3,
        'ammo': 'Shells',
        'strength': 2
    },

    'Rocket Launcher': {
        'name': 'Rocket Launcher',
        'id': 5,
        'ammo': 'Rockets',
        'strength': 3
    },
    'BFG?': {
        'name': 'BFG?',
        'id': 5,
        'ammo': 'Cells',
        'strength': 4
    }
}


def rankWeaponsBasedOnAvailabityAndAmmo(me):
    weapons = [v for (k,v) in WEAPONS.items() if me.weapons[k] == True and me.ammo[v['ammo']] > 0 ]
    #print(weapons)
    weapons = sorted(weapons, key = lambda w: w['strength'], reverse=True)
    #print("My weapons: " + str(weapons))
    return weapons




def getDistance(x1, y1, x2 ,y2):
        dis = math.sqrt((x1-x2)  ** 2 + (y1-y2) ** 2)
        return dis


#Default
polNothing = Policy(lambda world: 1, lambda world, agent: print("Nothing to do"), "Nothing")


#Dying
def polDeadUtility(world):
    print(world.getMe().health)
    return int(world.getMe().health <= 0) * 10**20

def polDeadExecute(world, agent):
    #Need to fix this shit
    agent.api.sendAction("use")
    sleep(1)
    me = agent.api.getPlayerInfo()
    world.resetMe(me)
    print("Come back to life bezos")

polDead = Policy(polDeadUtility, polDeadExecute, "Resurecting Bezos")


#Weapons
def polBFGUtility(world):
    if world.findClosestObjectByType('BFG?') is not None:
        return 1000 *int(world.getMe().weapons['BFG?'] == False)
    else:
        return 0


def polBFGExecute(world, agent):
    closestChainsaw = world.findClosestObjectByType('BFG?')
    agent.goTo(closestChainsaw.x, closestChainsaw.y)


polBFG = Policy(polBFGUtility, polBFGExecute, "Grabing a BFG")


def polShotgunUtility(world):
    if world.findClosestObjectByType('Shotgun') is not None:
        return 500 *int(world.getMe().weapons['Shotgun'] == False)
    else:
        return 0



def polShotgunExecute(world, agent):
    closestChainsaw = world.findClosestObjectByType('Shotgun')
    agent.goTo(closestChainsaw.x, closestChainsaw.y)


polShotGun = Policy(polShotgunUtility, polShotgunExecute, "Grabing a Shotgun")



def polChainsawUtility(world):
    if world.findClosestObjectByType('Chainsaw') is not None:
        return 200 *int(world.getMe().weapons['Chainsaw'] == False)
    else:
        return 0


def polChainsawExecute(world, agent):
    closestChainsaw = world.findClosestObjectByType('Chainsaw')
    agent.goTo(closestChainsaw.x, closestChainsaw.y)

polChainsaw= Policy(polChainsawUtility, polChainsawExecute, "Grabing a Chainsaw")



def polChooseWeaponUtility(world):
    me = world.getMe()
    weapons = rankWeaponsBasedOnAvailabityAndAmmo(me)
    if len(weapons) <= 0:
        return 1
    print("Current WeaponID: " + str(me.currentWeapon))
    print("Projected One: " + str(weapons[0]['id']))
    if weapons[0]['id']  != me.currentWeapon + 1:

        return 10**10
    else:
        return 0

def polChooseWeaponExecute(world, agent):
    me = world.getMe()
    weapons = rankWeaponsBasedOnAvailabityAndAmmo(me)
    id = weapons[0]['id']
    print("Changing weapon to " + str(weapons[0]))

    agent.me.setCurrentWeapon = id
    agent.api.sendAction('switch-weapon', id) #Magic Number af


polChooseWeapon = Policy(polChooseWeaponUtility, polChooseWeaponExecute, "Changing weapon")

#Ammo
def polShotgunShellsUtility(world):
    if world.findClosestObjectByType('Shotgun shells') is not None and world.getMe().weapons['Shotgun'] == True and world.getMe().ammo['Shells'] <=0:
        return 1000 *int(world.getMe().weapons['Chainsaw'] == False)
    else:
        return 0


def polShotgunShellsExecute(world, agent):
    closestShells = world.findClosestObjectByType('Shotgun shells')
    agent.goTo(closestShells.x, closestShells.y)

polShotgunShells= Policy(polShotgunShellsUtility, polShotgunShellsExecute, "Grabing a shells")


#Shooting
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
    if distance > 150:
        agent.goTo(closest.x, closest.y)
    else:
        print("Too Close!!")
        agent.face(closest.x, closest.y)
    print(str(agent.goToCleared))
    if (distance < 1000 and agent.goToCleared) or distance < 200:
        print("Angle of shooting: " + str(abs(agent.me.angleToPos(closest.x, closest.y))))
        if abs(agent.me.angleToPos(closest.x, closest.y)) < 30:
            if(agent.api.moveTest(agent.me.id, closest.x , closest.y)):
                agent.api.sendAction("shoot")
    
polShootPlayer = Policy(polShootPlayerUtility, polShootPlayerExecute, "Killing players")


def polShootPlayerLowLifeUtility(world):
    closePlayers = world.rankPlayersByDistance()
    closest = closePlayers[0]
    if closest.health < 40:
        me = world.getMe()
        return (getDistance(closest.x, closest.y, me.x, me.y) < 10000) * 2000
    else:
        return 1
    
polShootPlayerLowLife = Policy(polShootPlayerLowLifeUtility, polShootPlayerExecute, "Killing low life players")

#Green armor 100%

#polChooseWeapon
Policies = [polNothing, polDead, polShotGun, polChainsaw, polBFG, polShootPlayer, polShootPlayerLowLife, polChooseWeapon, polShotgunShells]