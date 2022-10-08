from npc_utils.npc_base import npc 
from general_utils.item_class import item
import random
import copy

class lumberjack(npc):
    def __init__(self,fname,sname):
        super().__init__(fname,sname)
        self.schedule = ['sleep','sleep','sleep','sleep','sleep','sleep','talk','talk','talk','job','job','job','job','job','job','job','job','sell','buy','talk','talk','eat','sleep','sleep']
        self.gather('Axe',1)
        self.job_title = 'lumberjack'
    def job(self):
        if self.stamina[0] > (self.strength[0]//3)+2:
            if 'Axe' in self.inventory.keys():
                self.gather('Hard wood',self.strength[0]//3)
                self.gather('Twigs',1)
                self.useitem('Axe')
            else:
                self.gather('Twigs',self.strength[0]//2)
                self.addneed('Axe',1,additive=False)
            self.usestat(self.strength,self.strength[0]//4)
            self.usestamina(self.strength[0]//3)
            
    def jobsell(self,world):
        if 'Hard wood' in self.inventory.keys():
            self.sell('Hard wood',self.inventory['Hard wood'].amount,self.inventory['Hard wood'].value,world)
        if 'Twigs' in self.inventory.keys():
            self.sell('Twigs',self.inventory['Twigs'].amount,self.inventory['Twigs'].value,world)
