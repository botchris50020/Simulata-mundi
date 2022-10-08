from npc_utils.npc_base import npc 
from general_utils.item_class import item
import random
import copy

class miner(npc):
    def __init__(self,fname,sname):
        super().__init__(fname,sname)
        self.schedule = ['sleep','sleep','sleep','sleep','sleep','sleep','talk','talk','talk','job','job','job','job','job','job','job','job','sell','buy','talk','talk','eat','sleep','sleep']
        self.gather('Pickaxe',1)
        self.job_title = 'miner'

    def job(self):
        if self.stamina[0] > (self.strength[0]//3)+2:
            if 'Pickaxe' in self.inventory.keys():
                self.gather('Iron Ore',self.strength[0]//3)
                self.useitem('Pickaxe')
            else:
                self.gather('Bloody Iron Ore',self.strength[0]//8)
                self.addneed('Pickaxe',1,additive=False)
            self.usestat(self.strength,self.strength[0]//3)
            self.usestamina(self.strength[0]//3)
    def jobsell(self,world):
        if 'Iron Ore' in self.inventory.keys():
            self.sell('Iron Ore',self.inventory['Iron Ore'].amount,self.inventory['Iron Ore'].value,world)
        if 'Bloody Iron Ore' in self.inventory.keys():
            self.sell('Bloody Iron Ore',self.inventory['Bloody Iron Ore'].amount,self.inventory['Bloody Iron Ore'].value,world)           
