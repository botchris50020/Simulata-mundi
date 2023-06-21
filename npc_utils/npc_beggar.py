from npc_utils.npc_base import npc 
from general_utils.item_class import item
import random
import copy

class beggar(npc):
    def __init__(self,fname,sname):
        super().__init__(fname,sname)
        self.schedule = ['sleep','sleep','sleep','sleep','sleep','sleep','talk','talk','talk','talk','talk','talk','talk','talk','talk','talk','talk','talk','buy','talk','talk','eat','sleep','sleep']
        self.job_title = 'beggar'
        self.begging_history = {}
    def whotalk(self,people):
        if self.stamina[0] > 5:
            options = []
            for p in people:
                if p.hp[0] > 0:
                    options.append(p)
            if len(options) > 0:
                favourability = []
                for i in options:
                    if i.name in self.relationships.keys():
                        favourability.append(self.relationships[i.name][1]+50)
                    else:
                        favourability.append(50)
                if sum(favourability) > 0:
                    person = random.choices(options,weights=favourability)[0]
                    self.talk(person)
                    person.talk(self)
                    if self.speech[0] > person.speech[0]:
                        if person.money > 10 and self.name in person.relationships.keys():
                            #print(max(10,int(person.money*((self.speech[0]*self.divinity[0])/100000))))
                            money_taken = max(12,int(person.money*((self.speech[0]*self.divinity[0])/400000)))
                            if not person.name in self.begging_history.keys():
                                self.begging_history[person.name] = [[money_taken,person.money]]
                            else:
                                self.begging_history[person.name].append([money_taken,person.money])
                            self.money += money_taken
                            self.relationships[person.name][1] += 1
                            person.money -= money_taken
                            person.relationships[self.name][1] -= 1
        else:
            self.stamina[0] += 5
