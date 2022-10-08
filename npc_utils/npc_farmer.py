from npc_utils.npc_base import npc 
from general_utils.item_class import item
import random
import copy

class farmer(npc):
    def __init__(self,fname,sname):
        super().__init__(fname,sname)
        self.schedule = ['sleep','sleep','sleep','sleep','sleep','sleep','talk','talk','talk','job','job','job','job','job','job','job','job','sell','buy','talk','talk','eat','sleep','sleep']
        self.gather('Hoe',1)
        self.job_title = 'farmer'
    def job(self):
        if self.stamina[0] > (self.strength[0]//6)+(self.dexterity[0]//8)+2:
            if 'Hoe' in self.inventory.keys():
                self.gather('Oats',int((self.strength[0]/6)+(self.dexterity[0]/6)))
                self.useitem('Hoe')
            else:
                self.gather('Oats',int((self.strength[0]/8)+(self.dexterity[0]/8)))
                self.addneed('Hoe',1,additive=False)
            self.usestat(self.strength,self.strength[0]//7)
            self.usestat(self.dexterity,self.dexterity[0]//7)
            self.usestamina(self.strength[0]//6)
            self.usestamina(self.dexterity[0]//8)
    def jobsell(self,world):
        if 'Oats' in self.inventory.keys():
            self.sell('Oats',self.inventory['Oats'].amount,self.inventory['Oats'].value,world)
