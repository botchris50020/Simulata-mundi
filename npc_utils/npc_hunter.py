from npc_utils.npc_base import npc 
from general_utils.item_class import item
import random
import copy

class hunter(npc):
    def __init__(self,fname,sname):
        super().__init__(fname,sname)
        self.schedule = ['sleep','sleep','sleep','sleep','sleep','sleep','talk','talk','talk','job','job','job','job','job','job','job','job','sell','buy','talk','talk','eat','sleep','sleep']
        self.gather('Bow',1)
        self.gather('Arrow',10)
        self.job_title = 'hunter'
    def job(self):
        if self.stamina[0] > (self.perception[0]//8)+(self.dexterity[0]//5)+2:
            if 'Bow' in self.inventory.keys() and 'Arrow' in self.inventory.keys():
                self.gather('Deer Meat',int((self.perception[0]/5)+(self.dexterity[0]/6)))
                self.useitem('Bow')
                luck_roll = random.randint(0,10)
                if luck_roll < 3:
                    self.useitem('Arrow')
                luck_roll = random.randint(0,self.perception[1]+5)
                if luck_roll > self.perception[0]:
                    self.damage(luck_roll-self.perception[0])
            else:
                self.gather('Rabbit Meat',int((self.perception[0]/6)+(self.dexterity[0]/10)))
                if not ('Bow' in self.inventory.keys()):
                    self.addneed('Bow',1,additive=False)
                if not ('Arrow' in self.inventory.keys()):
                    self.addneed('Arrow',10,additive=False)

            self.usestat(self.strength,self.perception[0]//6)
            self.usestat(self.dexterity,self.dexterity[0]//6)
            self.usestamina(self.perception[0]//8)
            self.usestamina(self.dexterity[0]//5)
    def jobsell(self,world):
        if 'Deer Meat' in self.inventory.keys():
            self.sell('Deer Meat',self.inventory['Deer Meat'].amount,self.inventory['Deer Meat'].value,world)
        if 'Rabbit Meat' in self.inventory.keys():
            self.sell('Rabbit Meat',self.inventory['Rabbit Meat'].amount,self.inventory['Rabbit Meat'].value,world)
