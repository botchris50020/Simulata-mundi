from npc_utils.npc_base import npc 
from general_utils.item_class import item
import random
import copy
import json

class blacksmith(npc):
    def __init__(self,fname,sname):
        super().__init__(fname,sname)
        self.schedule = ['sleep','sleep','sleep','sleep','sleep','sleep','talk','talk','talk','job','job','job','job','job','job','job','job','sell','buy','talk','talk','eat','sleep','sleep']
        self.gather('Hammer',1)
        self.job_title = 'blacksmith'
        self.making = ['',0,1,False]
        self.money = 500
    def job(self,world):
        if self.making[1] < self.making[2]:
            if world.blacksmith_needs == {}:
                item_to_make = item('Hoe')
            else:
                item_to_make = item(sorted(list(map(lambda a : [world.blacksmith_needs[a],a],world.blacksmith_needs)),key=lambda a : a[0])[-1][1])
            self.making = [item_to_make.name,item_to_make.durability[1],min(item_to_make.durability[1],0),False]

        if not self.making[3]:
            recipedata = json.load(open("recipes.json"))['blacksmith']
            crafted = True
            for i in recipedata[self.making[0]]:
                #print(i,recipedata[itemname][i])
                if not i in self.inventory.keys() or self.inventory[i].amount < recipedata[self.making[0]][i]:
##                    print(i,item(i).value,recipedata[itemname][i])
                    if i in self.inventory.keys():
                        self.buy(i,(recipedata[self.making[0]][i]-self.inventory[i].amount)+1,world)
                    else:
                        self.buy(i,recipedata[self.making[0]][i]+1,world)
                    crafted = False

            if crafted == True:
                for i in recipedata[self.making[0]]:
                    #print(i,recipedata[itemname][i])
                    self.inventory[i].amount -= recipedata[self.making[0]][i]
                self.making[3] = True

        if self.making[3]:
            if self.stamina[0] > (self.strength[0]//3)+2:
                if 'Hammer' in self.inventory.keys():
                    if self.making[2] < 0:
                        self.making[2] += int(self.speed[0]*(self.strength[0]/10))
                        self.gather(self.making[0],int(self.speed[0]*(self.strength[0]/10)))
                        self.usestat(self.speed,self.speed[0])
                        self.usestat(self.strength,self.strength[0]//10)
                        self.usestamina(int(self.speed[0]*(self.strength[0]/10))//5)
                    else:
                        self.making[2] += int((self.speed[0]/2)*(self.strength[0]/2))
                        self.usestat(self.speed,self.speed[0]//3)
                        self.usestat(self.strength,self.strength[0]//3)
                        self.usestamina(int((self.speed[0]/2)*(self.strength[0]/2))//10)
                        if self.making[1] < self.making[2]:
                            self.gather(self.making[0],1)
        
    def jobsell(self,world):
        if 'Pickaxe' in self.inventory.keys():
            self.sell('Pickaxe',self.inventory['Pickaxe'].amount,self.inventory['Pickaxe'].value,world)
        if 'Hoe' in self.inventory.keys():
            self.sell('Hoe',self.inventory['Hoe'].amount,self.inventory['Hoe'].value,world)
        if 'Bow' in self.inventory.keys():
            self.sell('Bow',self.inventory['Bow'].amount,self.inventory['Bow'].value,world)
        if 'Axe' in self.inventory.keys():
            self.sell('Axe',self.inventory['Axe'].amount,self.inventory['Axe'].value,world)
        if 'Arrow' in self.inventory.keys():
            self.sell('Arrow',self.inventory['Arrow'].amount,self.inventory['Arrow'].value,world)

    def dowhat(self,time,people,world):
        people = copy.copy(people)
        people.remove(self)
        #print(self.name,self.schedule[time])
        if self.hp[0] > 0:
            if self.schedule[time] == 'sleep':
                self.sleep()
            
            elif self.schedule[time] == 'talk':
                self.whotalk(people)

            elif self.schedule[time] == 'eat':
                self.what_to_eat()

            elif self.schedule[time] == 'buy':
                self.buyneeds(world)
            
            elif self.schedule[time] == 'job':
                self.job(world)

            elif self.schedule[time] == 'sell':
                self.jobsell(world)
                
