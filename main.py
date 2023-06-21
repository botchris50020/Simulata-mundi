from npc_utils.npc_miner import miner
from npc_utils.npc_beggar import beggar
from npc_utils.npc_farmer import farmer
from npc_utils.npc_hunter import hunter
from npc_utils.npc_lumberjack import lumberjack
from npc_utils.npc_blacksmith import blacksmith

from general_utils.area_class import area

import random
fnames = ['john','anny','ava','ada','katie','oliver','christian','tom','josh']
snames = ['smith','weekes','lord','brown','normann','balter','brighton','cadabra','loh']
all_names = []
all_people = []
for f in fnames:
    for s in snames:
        all_names.append([f,s])

world = area('tobi')
farmers = 6
hunters = 2
blacksmiths = 2
miners = 2
lumberjacks = 2
beggars = 1

##name = ['josh' ,'brown']
##all_names.remove(name)
##all_people.append(beggar(name[0],name[1]))
##all_people[0].divinity[1] += 1
for i in range(farmers):
    name = random.choice(all_names)
    all_names.remove(name)
    all_people.append(farmer(name[0],name[1]))

for i in range(hunters):
    name = random.choice(all_names)
    all_names.remove(name)
    all_people.append(hunter(name[0],name[1]))
    
for i in range(blacksmiths):
    name = random.choice(all_names)
    all_names.remove(name)
    all_people.append(blacksmith(name[0],name[1]))
    
for i in range(miners):
    name = random.choice(all_names)
    all_names.remove(name)
    all_people.append(miner(name[0],name[1]))
    
for i in range(lumberjacks):
    name = random.choice(all_names)
    all_names.remove(name)
    all_people.append(lumberjack(name[0],name[1]))

for i in range(beggars):
    name = random.choice(all_names)
    all_names.remove(name)
    all_people.append(beggar(name[0],name[1]))


    
random.shuffle(all_people)
print(list(map(lambda a: a.name,all_people)))

name = random.choice(all_names)
all_names.remove(name)
##a = miner("john",'smith')
##b = miner('anny','brighton')
##c = farmer('ava','cadabra')
##d = farmer('ada','avadra')



def timestep(k):
    for person in all_people:
        person.dowhat(k,all_people,world)
        
def oneday():
    world.think(all_people)
    for k in range(24):
        timestep(k)

def week():
    for i in range(6):
        oneday()
        
def month():
    for i in range(4):
        week()
    world.rent(all_people)

def year():
    for i in range(14):
        month()
    checkin()
        
def checkin():
    for i,p in enumerate(all_people):
        print(f'{i:<2} {p.name:<25}{p.job_title:<15}{p.money:>10}    {p.hp}')

def all_money():
    p_money = 0
    for person in all_people:
        p_money += person.money
    print(p_money)
    print(p_money+world.money)
def worldinv():
    print(world.money)
    for item in world.inventory:
        print(world.inventory[item].name,world.inventory[item].amount)
