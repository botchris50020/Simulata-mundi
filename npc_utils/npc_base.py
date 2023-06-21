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
            
        self.house = {}
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
##        self.history = []
        #self.equipment = {"head":[],"body":[],"right":[],"left":[],"legs":[],"shoes":[]}

    def summary(self):
        """
        prints out a nice summary of the npc
        """
        print(f'{"Name:":<6} {self.name:20}')
        print(f'Hp: {self.hp[0]}/{self.hp[1]}   Hunger: {self.hunger[0]}/{self.hunger[1]}')
        print(f'{"Job:":<6} {self.job_title:11} {"Money:":<6} {self.money}')
        print(f'')
        print(f'{"Int:":<10}{self.intelligence[0]:>4} {"Speech:":<10}{self.speech[0]:>4}')
        print(f'{"Str:":<10}{self.strength[0]:>4} {"Per:":<10}{self.perception[0]:>4}')
        print(f'{"Speed:":<10}{self.speed[0]:>4} {"Dex:":<10}{self.dexterity[0]:>4}')
        print(f'{"Stamina:":<10}{self.perception[0]:>4} {"Luck:":<10}{self.luck[0]:>4}')
        print(f'{"Divinity:":<10}{self.divinity[0]:>4}')
        #print(f'int speech')
        for i in self.inventory:
            print(f'{self.inventory[i].name:<10} x {self.inventory[i].amount}')
        #print(self.inventory)
    def useitem(self,itemname,num=1):
        """
        itemname str: Name of the item in the npc's inventory to use
        num int: number of that item to use

        It decreases the items durability by one and destroys the item if the durability reaches 0
        """
        if self.inventory[itemname].durability[1] > 0:
            for i in range(num):
                self.inventory[itemname].durability[0] -= 1
            if self.inventory[itemname].durability[0] <= 0:
                #print(itemname,'broke')
                self.discarditem(itemname,1)
        else:
            self.discarditem(itemname,num)

    def discarditem(self,itemname,num=1):
        """
        itemname str: Name of the item in the npc's inventory to use
        num int: number of that item to discard

        It removes one item of that name from the inventory, resetting its durability if there is another
        item with the same name in the inventory, else removing the name from the inventory
        """
        for i in range(num):
            self.inventory[itemname].amount -= 1
        if self.inventory[itemname].amount <= 0:
            del self.inventory[itemname]
        elif self.inventory[itemname].durability[1] > 0:
            self.inventory[itemname].durability[0] =  self.inventory[itemname].durability[1]

    def usestamina(self,amount):
        """
        amount int: amount of stamina to use

        removes the amount of stamina specified
        increases the total amount of stamina used
        if at less than half hunger, removes an additional stamina
        removes hunger equivalent to the amount of stamina used
        if less than 0 hunger, npc takes 5 damage
        """
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
        """
        amount int: amount of health to lose

        removes the amount of health specified
        increases the total amount of health lost
        """
        self.hp[0] -= amount
        self.hp[2] += amount

    def usestat(self,stat,amount):
        """
        stat list: pointer to the stat list to be used
        amount int: amount of the stat to use

        increases the total amount of that stat used
        """
        stat[2] += amount
        
    def addneed(self,need,amount,additive=True):
        """
        need str: name of the item that is needed
        amount int: amount of the item that is needed
        additive bool: if the need for that item stacks or not

        adds the need to the self.needs list, or increases the amount needed
        """
        if additive and need in self.needs.keys():
            self.needs[need].amount += amount
        else:
            self.needs[need] = item(need,amount=amount)


    # now defining all the basic actions an npc can take, each time, the action is taken for 1 hour
    def sleep(self):
        """
        if hunger is less than 0, npc takes 5 damage
        if the npc used a stat enough, it increases that stat, provided the stat ceiling isn't reached
        regenerate lost stat points if you are not starving (8 hours to fully regenerate)
        """
        if self.hunger[0] < 0:
            self.damage(5)
        for stat in self.stats:
            if stat[2] >= stat[1]*50 and stat[1] < self.statmax:
                stat[2] -= stat[1]*50
                stat[1] += 1
            elif stat[2] >= stat[1]**2:
                stat[2] -= stat[1]**2
                stat[1] += 1
                
            if stat[0] != stat[1] and self.hunger[0] > 0:
                stat[0] += max(1,(stat[1]//8)*self.divinity[0])
                if stat[0] > stat[1]:
                    stat[0] = stat[1]
        if self.stamina[2] >= self.stamina[1]*50 and self.stamina[1] < self.statmax*10:
            self.stamina[2] -= self.stamina[1]*50
            self.stamina[1] += 1
            self.hunger[1] = self.stamina[1]*3

    def talk(self, target):
        """
        target npc: the npc to talk to

        npc1 talks to npc2, if this is the first time talking, they will form an opinion
        this opinion can go up or down depending on if npc2 thinks highly or lowly of npc1
        """
        if self.stamina[0] < 5:
            self.stamina[0] += 5
        else:
            if target.name in self.relationships.keys() and self.name in target.relationships.keys():
                self.relationships[target.name][1] += ((self.speech[0]*self.divinity[0])*
                                                       self.relationships[target.name][0]+
                                                       (target.speech[0]*target.divinity[0])*
                                                       target.relationships[self.name][0])/100
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
                self.relationships[target.name][1] += (target.speech[0]*target.divinity[0])* \
                                                        self.relationships[target.name][0]
            self.usestat(self.speech,1)
            self.usestamina(1)

##    def request(self,text_options= [["is in need of","wants","asks you to provide","begs you to bring"],["as compensation","to make it worth your while","as payment","to ensure swift completion of the request"]]):
##        r = [] # form of a request: description (text in form: [name] is looking for [amount] [item]. [Name] is offering [reward] as compensation), needs, reward
##        need_text = ''
##        reward_text = ''
##        reward = {}
##        description = self.name+' '+random.choice(text_options[0])+need_text+'. '+self.name+' is offering '+reward_text+' '+random.choice(text_options[1])+'.'
##        r = [description,self.needs,reward]
##        return r
##    
    def gather(self,itemname,amount):
        """
        itemname str: the name of the item that is being gathered
        amount int: the amount of the item that gets gathered

        adds the amount of the item gathered to the inventory
        """
        if itemname in self.inventory.keys():
            self.inventory[itemname].amount += amount
        else:
            self.inventory[itemname] = item(itemname)
            self.inventory[itemname].amount = amount
        return True
    
    def make(self,itemname,recipe):
        """
        itemname str: the name of the item that is to be made
        recipe list: the list of ingredients needed to make the item

        if all the ingredients needed to craft the item are there, it will make the item
        """
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
        """
        itemname str: the name of the item that is to be bought
        amount int: the amount of that item to be bought
        world area: the area object that the npc is in

        if the npc has enough money and the area has enough of it,
            it will buy the amount of the item it has requested
        """
        price = 0
        if world != '':
                price = world.ask_buy(itemname,amount)
        if price > 0 and self.money >= price:
            world.sell(itemname,amount,price)
##            self.history.append([itemname,price,self.money])
            if price != 0 and world == '':
                print(self.name,'bought',item.name,'and it was not in the world')
            self.gather(itemname,amount)
            #print('bought',itemname)
            self.money -= price
            
            return True
        return False
    
    def buyneeds(self,world):
        """
        world area: the area object that the npc is in

        the npc goes through its list of needs and tries to buy everything on it
        """
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
        """
        itemname str: the name of the item that is to be sold
        amount int: the amount of that item to be sold
        price int: the price at which to sell the item
        world area: the area object that the npc is in

        the npc tries to sell its items to the area
        """
        if world.buy(itemname,amount,price):
            if itemname in self.inventory.keys() and self.inventory[itemname].amount >= amount:
                self.discarditem(itemname,amount)
                self.money += amount*price

    def eat(self,food):
        """
        food str: the name of the food that is to be eaten

        the npc tries to eat the food item to refill its hunger
        """
        if food in self.inventory.keys() and 'hunger' in self.inventory[food].properties.keys():
            self.hunger[0] += self.inventory[food].properties['hunger']
            self.useitem(food)
        if self.hunger[0] > self.hunger[1]:
            self.hunger[0] = self.hunger[1]

    def what_to_eat(self):
        """
        decides what the npc wants/needs to eat to sustain itself
        """
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
        """
        world area: the area the npc is in
        
        decides what foods to buy to best feed the npc
        """
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
        """
        people list: a list of people that the npc could talk to

        decides who to talk to based on how much it likes the people around it
        """
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
        """
        time int: the time of day it is
        people list: a list of all the npc's nearby
        world area: the area the npc is in

        causes the npc one hunger, then if it's alive, it does what its schedule says it should.
        also announces the death on any npc
        """
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
