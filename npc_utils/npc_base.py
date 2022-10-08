from general_utils.item_class import item 
import random
import copy

class npc():
    def __init__(self,fname,sname,name='',mstats=[12,12,12,12,12,12,30,1,1]):
        self.fname = fname
        self.sname = sname
        if name == '':
            self.name = fname+' '+sname
        else:
            self.name = name
        statpoints = 18
        stats = copy.copy(mstats)
        for i in range(len(stats)-3):
            if statpoints >= 6:
                add = random.randint(0,6)
            else:
                add = random.randint(0,statpoints)
            statpoints -= add
            stats[i] += add

        self.needs = {}
        self.hunger_today = 0
        self.job_title = ''
        self.inventory = {}
        self.money = 100
        self.location = ''
        self.relationships = {} # example relationship {"john smith":[-1,5]} in the form name:[like or not, total favourability]
        self.intelligence = [stats[0]] *3 # stats are in the form [current,max,times_used]
        self.speech = [stats[1]]*3
        self.strength = [stats[2]]*3
        self.perception = [stats[3]]*3
        self.speed = [stats[4]]*3
        self.dexterity = [stats[5]]*3
        self.stamina = [stats[6]]*3
        self.luck = [stats[7]]*3
        self.luck[2] = 0
        self.divinity = [stats[8]]*3
        self.divinity[2] = 0
        self.hp = [self.strength[1]+self.stamina[1]]*3
        self.stats = [self.intelligence,self.speech,self.strength,self.perception,self.speed,self.dexterity,self.stamina,self.luck,self.divinity,self.hp]
        self.statmax = 30
        self.hunger = [self.stamina[0]*3,self.stamina[0]*3]
        #self.statpoints = sp
        self.schedule = ['','','','','','','','','','','','','','','','','','','','','','','','']
        self.experience = 0
        self.level = 0
        self.dead = False
        #self.equipment = {"head":[],"body":[],"right":[],"left":[],"legs":[],"shoes":[]}
    def useitem(self,itemname,num=1):
        if self.inventory[itemname].durability[1] > 0:
            for i in range(num):
                self.inventory[itemname].durability[0] -= 1
            if self.inventory[itemname].durability[0] <= 0:
                #print(itemname,'broke')
                self.discarditem(itemname,1)
        else:
            self.discarditem(itemname,num)

    def discarditem(self,itemname,num=1):
        for i in range(num):
            self.inventory[itemname].amount -= 1
        if self.inventory[itemname].amount <= 0:
            del self.inventory[itemname]
        elif self.inventory[itemname].durability[1] > 0:
            self.inventory[itemname].durability[0] =  self.inventory[itemname].durability[1]

    def usestamina(self,amount):
        self.stamina[0] -= amount
        self.stamina[2] += amount
        if self.hunger[0] < self.hunger[1]/2:
            self.stamina[0] -= 1
        self.hunger[0] -= amount
        if self.stamina[0] < 0:
            self.damage(self.stamina[0]*-1)
        if self.hunger[0] < 0:
            self.damage(5)

    def damage(self,amount):
        self.hp[0] -= amount
        self.hp[2] += amount

    def usestat(self,stat,amount):
        stat[2] += amount
        
    def addneed(self,need,amount,additive=True):
        if additive and need in self.needs.keys():
            self.needs[need].amount += amount
        else:
            self.needs[need] = item(need,amount=amount)
    # now defining all the basic actions an npc can take, each time, the action is taken for 1 hour
    def sleep(self):
        if self.hunger[0] < 0:
            self.damage(5)
        for stat in self.stats:
            if stat[2] >= stat[1]*50 and stat[1] < self.statmax: # gain extra points if you've used that stat enough
                stat[2] -= stat[1]*50
                stat[1] += 1
            elif stat[2] >= stat[1]**2:
                stat[2] -= stat[1]**2
                stat[1] += 1
                
            if stat[0] != stat[1] and self.hunger[0] > 0: # regenerate your lost stat points if you aren't starving
                stat[0] += max(1,(stat[1]//8)*self.divinity[0])
                if stat[0] > stat[1]:
                    stat[0] = stat[1]
        if self.stamina[2] >= self.stamina[1]*50 and stat[1] < self.statmax*10:
            self.stamina[2] -= self.stamina[1]*50
            self.stamina[1] += 1
            self.hunger[1] = self.stamina[1]*3

    def talk(self, target):
        if self.stamina[0] < 5:
            self.stamina[0] += 5
        else:
            if target.name in self.relationships.keys() and self.name in target.relationships.keys():
                self.relationships[target.name][1] += ((self.speech[0]*self.divinity[0])*self.relationships[target.name][0] + (target.speech[0]*target.divinity[0])*target.relationships[self.name][0])/100
            else:
                self.relationships[target.name] = [0,0]
                if target.speech[1] >= 30:
                    temp = target.speech[1]+10
                else:
                    temp = 30
                if random.randint(0,temp) > target.speech[1]:
                    self.relationships[target.name][0] = -1
                else:
                    self.relationships[target.name][0] = 1
                self.relationships[target.name][1] += (target.speech[0]*target.divinity[0])*self.relationships[target.name][0]
            self.usestat(self.speech,1)
            self.usestamina(1)

    def request(self,text_options= [["is in need of","wants","asks you to provide","begs you to bring"],["as compensation","to make it worth your while","as payment","to ensure swift completion of the request"]]):
        r = [] # form of a request: description (text in form: [name] is looking for [amount] [item]. [Name] is offering [reward] as compensation), needs, reward
        need_text = ''
        reward_text = ''
        reward = {}
        description = self.name+' '+random.choice(text_options[0])+need_text+'. '+self.name+' is offering '+reward_text+' '+random.choice(text_options[1])+'.'
        r = [description,self.needs,reward]
        return r
    
    def gather(self,itemname,amount):
        if itemname in self.inventory.keys():
            self.inventory[itemname].amount += amount
        else:
            self.inventory[itemname] = item(itemname)
            self.inventory[itemname].amount = amount
        return True
    
    def make(self,itemname,recipe):
        canmake = True
        for ingredient in recipe:
            if not (ingredient in self.inventory.keys() and self.inventory[ingredient] >= recipe[ingredient]):
                canmake = False
        if canmake:
            for ingredient in recipe:
                self.inventory[ingredient] -= recipe[ingredient]
            return item(itemname)
        return ''
    
    def buy(self,itemname,amount,world=''):
        if world != '':
                price = world.ask_buy(itemname,amount)
        if price > 0 and self.money >= price:
            world.sell(itemname,amount,price)
            if price != 0 and world == '':
                print(self.name,'bought',item.name,'and it was not in the world')
            self.gather(itemname,amount)
            #print('bought',itemname)
            self.money -= price
            return True
        return False
    
    def buyneeds(self,world):
        self.buyfood(world)
        fulfilled = {}
        for need in self.needs:
            for i in range(self.needs[need].amount):
                if self.buy(need,1,world):
                    if need in fulfilled.keys():
                        fulfilled[need] += 1
                    else:
                        fulfilled[need] = 1
        for done in fulfilled:
            for numdone in range(fulfilled[done]):
                self.needs[done].amount -= 1
                
    def sell(self,itemname,amount,price,world):
        if world.buy(itemname,amount,price):
            if itemname in self.inventory.keys() and self.inventory[itemname].amount >= amount:
                self.discarditem(itemname,amount)
                self.money += amount*price

    def eat(self,food):
        if food in self.inventory.keys() and 'hunger' in self.inventory[food].properties.keys():
            self.hunger[0] += self.inventory[food].properties['hunger']
            self.useitem(food)
        if self.hunger[0] > self.hunger[1]:
            self.hunger[0] = self.hunger[1]

    def what_to_eat(self):
        has_to_eat = self.hunger[1]-self.hunger[0]
        self.hunger_today = self.hunger[1]-self.hunger[0]
        while 'Feast' in self.inventory.keys() and has_to_eat >= 100:
            self.eat('Feast')
            has_to_eat -= 150

        while 'Large Meal' in self.inventory.keys() and has_to_eat >= 50:
            self.eat('Large Meal')
            has_to_eat -= 100
        
        while 'Filling Meal' in self.inventory.keys() and has_to_eat >= 30:
            self.eat('Filling Meal')
            has_to_eat -= 50
        while 'Small Meal' in self.inventory.keys() and has_to_eat >= 10:
            self.eat('Small Meal')
            has_to_eat -= 30

        
        
            
    def buyfood(self,world):
        failed = False
        while self.hunger_today >= 100 and not failed:
            if self.buy('Feast',1,world):
                self.hunger_today -= 150
            else:
                failed = True
        failed = False
        while self.hunger_today >= 50 and not failed:
            if self.buy('Large Meal',1,world):
                self.hunger_today -= 100
            else:
                failed = True
        failed = False
        while self.hunger_today >= 30 and not failed:
            if self.buy('Filling Meal',1,world):
                self.hunger_today -= 50
            else:
                failed = True
        failed = False
        while self.hunger_today >= 10 and not failed:
            if self.buy('Small Meal',1,world):
                self.hunger_today -= 30
            else:
                failed = True

    def whotalk(self,people):
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
            else:
                self.stamina[0] += 5

    def job(self):
        pass

    def jobsell(self,world):
        pass

    def dowhat(self,time,people,world):
        self.hunger[0] -= 1
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
                self.job()

            elif self.schedule[time] == 'sell':
                self.jobsell(world)
        elif not self.dead:
            print(self.name,'has Died! They were a',self.job_title,'. It is Day:',world.day)
            try:
                print(self.money,self.hunger,world.inventory['Oats'].amount,world.inventory['Deer Meat'].amount)
            except KeyError:
                print(self.money,self.hunger,'No food')
            self.dead = True
