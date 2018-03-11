import math
import time
from time import sleep
from policy import Policy
import copy
import random




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

WEAPONS_FORK = copy.deepcopy(WEAPONS)
WEAPONS_FORK['Rocket Launcher']['strength'] = 0


def rankWeaponsBasedOnAvailabityAndAmmo(me):
    weapons = [v for (k,v) in WEAPONS.items() if me.weapons[k] == True and me.ammo[v['ammo']] > 0 ]
    
    if getDistance(me.x, me.y, -1325, -541) > 2600:
        print("Distance from the center " + str(getDistance(me.x, me.y, -1325, -541)))
        print("FAR FROM THE CENTER")
        weapons = [v for (k,v) in WEAPONS_FORK.items() if me.weapons[k] == True and me.ammo[v['ammo']] > 0 ]

    #print(weapons)
    weapons = sorted(weapons, key = lambda w: w['strength'], reverse=True)
    print("My weapons: " + str(weapons))
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
    agent.setFreshness(0)
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



def polRLUtility(world):
    if world.findClosestObjectByType('Rocket launcher') is not None:
        rl = world.findClosestObjectByType('Rocket launcher')
        print("RL available: " + str(rl is not None))
        distance = rl.distanceFromPlayer
        print("Distance from RL " + str(distance))
        return 1000 *int(world.getMe().weapons['Rocket Launcher'] == False) * (int(distance < 1500) + 0.2)
    else:
        rl = world.findClosestObjectByType('Rocket launcher')
        print("RL available: " + str(rl is not None))
        return 0


def polRLExecute(world, agent):
    closestRL = world.findClosestObjectByType('Rocket launcher')
    agent.goTo(closestRL.x, closestRL.y)


polRL = Policy(polRLUtility, polRLExecute, "Grabing a Rocket Launcher")


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
        return 100 *int(world.getMe().weapons['Chainsaw'] == False)
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
    if world.findClosestObjectByType('Shotgun shells') is not None and world.getMe().weapons['Shotgun'] == True and world.getMe().ammo['Shells'] <=5:
        ammo = world.findClosestObjectByType('Shotgun shells')
        me = world.getMe()
        distance = getDistance(ammo.x, ammo.y, me.x, me.y)
        if distance < 3000:
            return 300
        elif world.getMe().ammo['Shells'] <= 1:
            return 350
        else:
            return 0
    else:
        return 0


def polShotgunShellsExecute(world, agent):
    closestShells = world.findClosestObjectByType('Shotgun shells')
    agent.goTo(closestShells.x, closestShells.y)

polShotgunShells= Policy(polShotgunShellsUtility, polShotgunShellsExecute, "Grabing shells")


def polBulletsUtility(world):
    if world.findClosestObjectByType('Ammo clip') is not None and world.getMe().weapons['Handgun'] == True and world.getMe().ammo['Bullets'] <= 10:
        ammo = world.findClosestObjectByType('Ammo clip')
        me = world.getMe()
        distance = getDistance(ammo.x, ammo.y, me.x, me.y)
        if distance < 3000:
            return 200
        elif world.getMe().ammo['Bullets'] <= 1:
            return 250
    else:
        return 0


def polBulletsExecute(world, agent):
    closestShells = world.findClosestObjectByType('Shotgun shells')
    agent.goTo(closestShells.x, closestShells.y)

polBullets= Policy(polBulletsUtility, polBulletsExecute, "Grabing bullets")




def polRocketUtility(world):
    if world.findClosestObjectByType('Box of Rockets') is not None and world.getMe().weapons['Rocket Launcher'] == True and world.getMe().ammo['Rockets'] <= 1:
        ammo = world.findClosestObjectByType('Box of Rockets')
        me = world.getMe()
        distance = getDistance(ammo.x, ammo.y, me.x, me.y)
        if distance < 3000:
            return 200
        elif world.getMe().ammo['Rockets'] <= 0:
            return 250
    else:
        return 0


def polRocketExecute(world, agent):
    closestShells = world.findClosestObjectByType('Box of Rockets')
    agent.goTo(closestShells.x, closestShells.y)

polRockets= Policy(polRocketUtility, polRocketExecute, "Grabing rockets")


#Shooting
def polShootPlayerInRectangleUtility(world):
    closePlayers = world.rankPlayersByDistance()
    playersInRectangle = []
    for p in closePlayers:
        if p.isInRectangle():
            playersInRectangle.append(p)

    if(len(playersInRectangle) == 0):
        print("No one in the rectangle")
        return 1
    closest = playersInRectangle[0]

    me = world.getMe()
    return (getDistance(closest.x, closest.y, me.x, me.y) < 10000) * 300 + (getDistance(closest.x, closest.y, me.x, me.y) < 2000) * 700

def shootSafe(agent):
    agent.api.sendAction('shoot')

def polShootPlayerInRectangleExecute(world, agent):
    closePlayers = world.rankPlayersByDistance()
    closePlayers = [x for x in closePlayers if x.isInRectangle()]
    me = world.getMe()
    if(len(closePlayers)== 0):
        return 0
    closest = closePlayers[0]
    p = closest
    angleBetweenUs = agent.me.angleToPos(p.x , p.y)
    distance = getDistance(agent.me.x, agent.me.y, p.x, p.y)
    safe_x , safe_y = agent.me.findCoordinates(angleBetweenUs, distance - 250)

    if(distance > 310):
        agent.goTo(safe_x, safe_y)
    else:
        agent.goToBackward(safe_x, safe_y, p.x, p.y)

    if distance < 800:
        shootSafe(agent)


polShootPlayerInRectangle = Policy(polShootPlayerInRectangleUtility, polShootPlayerInRectangleExecute, "Killing players in the rectangle")

def polShootPlayerUtility(world):
    closePlayers = world.rankPlayersByDistance()
    if(len(closePlayers)== 0):
        return 0
    closest = closePlayers[0]
    me = world.getMe()
    return (getDistance(closest.x, closest.y, me.x, me.y) < 10000) * 200 + (getDistance(closest.x, closest.y, me.x, me.y) < 2000) * 400

def polShootPlayerExecute(world, agent):
    players = world.rankPlayersByDistance()
    p = players[0]
    angleBetweenUs = agent.me.angleToPos(p.x , p.y)
    distance = getDistance(agent.me.x, agent.me.y, p.x, p.y)

    safe_x , safe_y = agent.me.findCoordinates(angleBetweenUs, distance - 250)

    if(distance > 310):
        agent.goTo(safe_x, safe_y)
    else:
        agent.goToBackward(safe_x, safe_y, p.x, p.y)

    if distance < 800:
        shootSafe(agent)
    
polShootPlayer = Policy(polShootPlayerUtility, polShootPlayerExecute, "Killing players")


def polShootPlayerLowLifeUtility(world):
    closePlayers = world.rankPlayersByDistance()
    if(len(closePlayers)== 0):
        return 0
    closest = closePlayers[0]
    if closest.health < 40:
        me = world.getMe()
        return (getDistance(closest.x, closest.y, me.x, me.y) < 5000) * 500 + (getDistance(closest.x, closest.y, me.x, me.y) < 2000) * 800
    else:
        return 1
    
polShootPlayerLowLife = Policy(polShootPlayerLowLifeUtility, polShootPlayerExecute, "Killing low life players")


#Armor
def polArmorUtility(world):
    print("Available Armor?: " + str(world.findClosestObjectByType('Green armor 100%') is not None))
    print("Armor: " + str(world.getMe().armor))
    if world.findClosestObjectByType('Green armor 100%') is not None and world.getMe().armor < 50:
        return 250
    else:
        return 0


def polArmorExecute(world, agent):
    closestArmor = world.findClosestObjectByType('Green armor 100%')
    agent.goTo(closestArmor.x, closestArmor.y)

polArmor= Policy(polArmorUtility, polArmorExecute, "Grabing an armor")
#Life
def polLifeUtility(world):
    print("Available Life?: " + str(world.findClosestObjectByType('Health Potion +1% health') is not None))
    print("Health: " + str(world.getMe().health))
    if world.findClosestObjectByType('Health Potion +1% health') is not None and world.getMe().health < 50:
        ammo = world.findClosestObjectByType('Health Potion +1% health')
        me = world.getMe()
        distance = getDistance(ammo.x, ammo.y, me.x, me.y)
        if distance < 1000:
            return 1000
        else:
            return 200
    else:
        return 0


def polLifeExecute(world, agent):
    closestLife = world.findClosestObjectByType('Health Potion +1% health')
    agent.goTo(closestLife.x, closestLife.y)

polLife= Policy(polLifeUtility, polLifeExecute, "Grabing a life")



#Test

def polTestStrafeUtility(world):
    closePlayers = world.rankPlayersByDistance()
    if(len(closePlayers)== 0):
        return 0
    closest = closePlayers[0]
    me = world.getMe()
    return (getDistance(closest.x, closest.y, me.x, me.y) < 10000) * 200 + (getDistance(closest.x, closest.y, me.x, me.y) < 2000) * 400

def polTestStrafeExecute(world, agent):
    players = world.rankPlayersByDistance()
    p = players[0]
    angleBetweenUs = agent.me.angleToPos(p.x , p.y)
    distance = getDistance(agent.me.x, agent.me.y, p.x, p.y)

    safe_x , safe_y = agent.me.findCoordinates(angleBetweenUs, distance - 300)

    if(distance > 310):
        agent.goTo(safe_x, safe_y)
    else:
        agent.goToBackward(safe_x, safe_y, p.x, p.y)
        agent.api.sendAction('shoot')
polStrafe= Policy(polTestStrafeUtility, polTestStrafeExecute, "testing strafe")



#Green armor 100%

#polChooseWeapon polStrafe
Policies = [polNothing, polDead, polShotGun, polChainsaw, polBFG, polShootPlayer, polShootPlayerLowLife, polShootPlayerInRectangle, polChooseWeapon, polShotgunShells, polBullets, polArmor, polLife, polRL, polRockets ]