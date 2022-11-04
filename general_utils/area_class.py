from general_utils.item_class import item
import json

class area():
    def __init__(self,name):
        self.name = name
        self.inventory = {}
        self.blacksmith_needs = {}
        self.money = 100000000
        self.gain = {}
        self.sold = {}
        self.day = 0
    def summary(self):
        print('Gained',self.gain)
        print('Sold',self.sold)
        print('Liquid',self.money)
        value = 0
        for item in self.inventory:
            value += self.inventory[item].value*self.inventory[item].amount
        print('Static',value)
        print('Total',value+self.money)

    def rent(self,people):
        for p in people:
            if not p.dead:
                if p.job_title == 'miner':
                    if p.money >= 3000:
                        p.money -= 3000
                        self.money += 3000
                    else:
                        self.money += p.money
                        p.money = 0
                elif p.job_title == 'lumberjack':
                    p.money -= 3000
                    self.money += 3000
                elif p.job_title == 'farmer':
                    p.money -= 1000
                    self.money += 1000
                elif p.job_title == 'hunter':
                    p.money -= 3000
                    self.money += 3000
                elif p.job_title == 'blacksmith':
                    p.money -= 4000
                    self.money += 4000

    def add_to_summary(self,item,num,sellorbuy):
        if sellorbuy == 'sell':
            if item in self.sold.keys():
                self.sold[item] += num
            else:
                self.sold[item] = num
        else:
            if item in self.gain.keys():
                self.gain[item] += num
            else:
                self.gain[item] = num
                
    def discarditem(self,itemname,num=1):
        for i in range(num):
            self.inventory[itemname].amount -= 1
##        if self.inventory[itemname].amount <= 0:
##            del self.inventory[itemname]

    def gather(self,itemname,amount):
        self.add_to_summary(itemname,amount,'buy')
        if itemname in self.inventory.keys():
            self.inventory[itemname].amount += amount
        else:
            self.inventory[itemname] = item(itemname)
            self.inventory[itemname].amount = amount
        return True
    
    def buy(self,itemname,amount,price):
        if self.money >= price*amount:
            self.gather(itemname,amount)
            self.money -= price*amount
            return True
        return False

    def ask_buy(self,itemname,amount):
        recipedata = json.load(open("recipes.json"))['world']
        price = 0
        if itemname in recipedata.keys():
            crafted = True
            for i in recipedata[itemname]:
                #print(i,recipedata[itemname][i])
                if i in self.inventory.keys() and self.inventory[i].amount >= amount*recipedata[itemname][i]:
##                    print(i,item(i).value,recipedata[itemname][i])
                    price += item(i).value*recipedata[itemname][i]
                else:
                    crafted = False
            if crafted:
##                print(itemname,'costs',price)
                return (amount*price)+((amount*price)//4)
        else:
            if itemname in self.inventory.keys() and self.inventory[itemname].amount >= amount:
                price = self.inventory[itemname].value
##                print(itemname,'costs',price)
                return (amount*price)+((amount*price)//4)
##            if itemname != 'Arrow':
##                print('There was no',itemname)
        return -1


    def sell(self,itemname,amount,price):
        recipedata = json.load(open("recipes.json"))['world']
        if itemname in recipedata.keys():
            for i in recipedata[itemname]:
                #print(i,recipedata[itemname][i],amount)
                if i in self.inventory.keys() and self.inventory[i].amount >= amount*recipedata[itemname][i]:
                    self.inventory[i].amount -= amount*recipedata[itemname][i]
                    #self.discarditem(itemname,amount)
            self.add_to_summary(itemname,amount,'sell')
            self.money += price
            return True
        else:
            if itemname in self.inventory.keys() and self.inventory[itemname].amount >= amount:
                self.inventory[itemname].amount -= amount
                self.add_to_summary(itemname,amount,'sell')
                self.money += price


    def fulfill_request(self,item):
        self.blacksmith_needs[item] -= 1
        
    def think(self,people):
        self.blacksmith_needs = {}
        for p in people:
            if not p.dead:
                if p.job_title == 'miner':
                    if 'Pickaxe' in  self.blacksmith_needs.keys():
                        self.blacksmith_needs['Pickaxe'] += 1
                    else:
                        self.blacksmith_needs['Pickaxe'] = 1
                        
                elif p.job_title == 'lumberjack':
                    if 'Axe' in  self.blacksmith_needs.keys():
                        self.blacksmith_needs['Axe'] += 1
                    else:
                        self.blacksmith_needs['Axe'] = 1
                    
                elif p.job_title == 'farmer':
                    if 'Hoe' in  self.blacksmith_needs.keys():
                        self.blacksmith_needs['Hoe'] += 1
                    else:
                        self.blacksmith_needs['Hoe'] = 1
                    
                elif p.job_title == 'hunter':
                    if 'Bow' in  self.blacksmith_needs.keys():
                        self.blacksmith_needs['Bow'] += 1
                    else:
                        self.blacksmith_needs['Bow'] = 1
                    if 'Arrow' in  self.blacksmith_needs.keys():
                        self.blacksmith_needs['Arrow'] += 10
                    else:
                        self.blacksmith_needs['Arrow'] = 10
        for item in self.inventory:
            if item in self.blacksmith_needs.keys():
                self.blacksmith_needs[item] -= self.inventory[item].amount
        #print(self.blacksmith_needs)
        self.day += 1
##        if self.gain != {}:
##            print('###########################')
##            print('Day:',self.day)
##            print('Gained',self.gain)
##            print('Sold',self.sold)
##            print('Liquid',self.money)
##            value = 0
##            for item in self.inventory:
##                value += self.inventory[item].value*self.inventory[item].amount
##            print('Static',value)
##            print('Total',value+self.money)
##            self.gain = {}
##            self.sold = {}
##            print('###########################')
        
                
