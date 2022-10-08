import json

class item():
    def __init__(self,name,value=0,damage=1,damage_type='blunt',properties={},amount=1,durability=-1):
        def initialize_attrib(attrib,attrib_str,standard,bd):
            if attrib != standard:
                return attrib
            elif attrib_str in bd.keys():
                return bd[attrib_str]
            else:
                return standard

        base_data = json.load(open("items.json"))[name]
        self.name = name
        self.amount = initialize_attrib(amount,'amount',1,base_data)
        self.value = initialize_attrib(value,'value',0,base_data)
        self.damage = initialize_attrib(damage,'damage',1,base_data)
        self.damage_type = initialize_attrib(damage_type,'damage_type','blunt',base_data)
        self.properties = initialize_attrib(properties,'properties',{},base_data)
        self.durability = [initialize_attrib(durability,'durability',-1,base_data)]*2
