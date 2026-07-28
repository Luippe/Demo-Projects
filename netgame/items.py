item_rarity = ['Common', 'Uncommon', 'Rare']

# ITEMS: [low, high)
# Common: 0~2
# Uncommon: 2~4
# Rare: 4~6

item_name_dict = {'item':{0:'BLUE OBJECT',
                            1:'test_item2',
                            2:'test_item3',
                            3:'test_item4',
                            4:'test_item5',
                            5:'test_item6'}}


item_description_dict = {'item':{0:'TEST TEST TEST TEST TEST.',
                                    1: 'An Item Made Solely For Testing Purposes. This Item Has Absolutely No Use. Cannot Be Sold.',
                                    2: 'QWEJOKJASDASDNASDNAKSDASD ASDKJALSDJASDKALKSD AJSKD JAL.',
                                    3: 'A Rare Item. You Should Keep It Just In Case. Because Its Rare',
                                    4: 'TEST TEST',
                                    5: 'TEST TEst Test'}}


#================ARMOR=======================
chest_armor = {0:'Steel Chest',
               1:'Wizards Robe',
               2:'Assassins Coat',
               3:'Shamans Coat'}
head_armor = {0:'Steel Head',
             1:'Wizards Hood',
             2:'Assassins Hood',
             3:'Shamans Hat'}
leg_armor = {0:'Steel Legs',
             1:'Wizards Waist',
             2:'Assassins Waist',
             3:'Shamans Waist'}
armor_name_dict = {'chest':chest_armor, 'head':head_armor, 'legs':leg_armor}


chest_description = {0:'Armor made from pure steel. Able to withstand the toughest hits',
                     1:'Robe once worn by a skilled wizard',
                     2:'An oddly suspicious hoodie and mask. Probably not a good idea to wear this into a bank',
                     3:'A coat without any pockets'}
head_description = {0:'Armor made from pure steel. Able to withstand the toughest hits',
                   1:'Hoodie once worn by a skilled wizard to hide its epic hair',
                   2:'Heat tech keeps you warm',
                   3:'Classic hat for all spell casters'}
leg_description = {0:'Armor made from pure steel. Able to withstand the toughest hits',
                   1:'A bit difficult to move in, but makes a good pajama',
                   2:'Make sure you dont get pick-pocketed',
                   3:'Extra large size. Requires a belt to hold it from falling down'}
armor_description_dict = {'chest':chest_description, 'head':head_description, 'legs':leg_description}


chest_stats = {0:{'Defense':1, 'Attack':0, 'Special':None},
               1:{'Defense':0, 'Attack':1, 'Special':None},
               2:{'Defense':0, 'Attack':1, 'Special':None},
               3:{'Defense':0, 'Attack':1, 'Special':None}}
head_stats = {0:{'Defense':3, 'Attack':0, 'Special':None},
             1:{'Defense':0, 'Attack':3, 'Special':None},
             2:{'Defense':0, 'Attack':1, 'Special':None}}
leg_stats = {0:{'Defense':1, 'Attack':0, 'Special':None},
             1:{'Defense':0, 'Attack':1, 'Special':None},
             2:{'Defense':0, 'Attack':1, 'Special':None},
             3:{'Defense':0, 'Attack':1, 'Special':None}}
#===========================================


#==================Weapons=================
weapon_name_dict = {'weapon':{0:'Red Sword',
                            1:'Blue Sword',
                            2:'Yellow Sword',
                            3:'Scythe',
                            4:'Dagger',
                            5:'Wooden Knuckles',
                            6:'Steel Knuckles',
                            7:'Wizard Staff',
                            8:'Shaman Staff',
                            9:'Leather Whip',
                            10:'Dual Whip'}}
weapon_description_dict = {'weapon':{0:'Red sword',
                                     1:'Blue sword',
                                     2:'Yellow sword',
                                     3:'Capable of dealing high damage in a straight line',
                                     4:'Capable of dealing high damage at close range',
                                     5:'Capable of dealing high damage at close range. Can be upgraded to the Steel Knuckles',
                                     6:'Capable of dealing high damage at close range',
                                     7:'A staff once held by a powerful mage. Capable of dealing damage in a large area. Its special move unleashes a large fire ball, dealing damage in a large area',
                                     8:'A staff forged by a skilled shaman. Despite its small melee damage, its special move is capable of healing players',
                                     9:'Capable of dealing high damage at long range',
                                     10:'Capable of dealing descent damage at mid range'}}
weapon_stats = {0:{'Defense':0, 'Attack':3, 'Area Linear':[[(1,1),(2,2),(3,3)],[(1,-1),(2,-2),(3,-3)]], 'Area Diag':[[(1,-1)]], 'delay':20, 'pierce':False, 'Special':'Crit', 'Special Data':[1], 'Special CD':2},
                1:{'Defense':0, 'Attack':4, 'Area Linear':[[(1,1),(2,2),(3,3)],[(1,-1),(2,-2),(3,-3)]], 'Area Diag':[[(1,-1)]], 'delay':20, 'pierce':False, 'Special':'Attack', 'Special Data':[[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], [[(1,-1)]], 0], 'Special CD':3},
                2:{'Defense':0, 'Attack':5, 'Area Linear':[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], 'Area Diag':[[(1,-1)]], 'delay':20, 'pierce':False, 'Special':None},
                3:{'Defense':0, 'Attack':10, 'Area Linear':[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], 'Area Diag':[[(1,-1)]], 'delay':0, 'pierce':False, 'Special':None},
                4:{'Defense':0, 'Attack':10, 'Area Linear':[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], 'Area Diag':[[(1,-1)]], 'delay':0, 'pierce':False, 'Special':None},
                5:{'Defense':0, 'Attack':10, 'Area Linear':[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], 'Area Diag':[[(1,-1)]], 'delay':0, 'pierce':False, 'Special':None},
                6:{'Defense':0, 'Attack':10, 'Area Linear':[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], 'Area Diag':[[(1,-1)]], 'delay':0, 'pierce':False, 'Special':None},
                7:{'Defense':0, 'Attack':10, 'Area Linear':[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], 'Area Diag':[[(1,-1)]], 'delay':0, 'pierce':False, 'Special':None},
                8:{'Defense':0, 'Attack':10, 'Area Linear':[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], 'Area Diag':[[(1,-1)]], 'delay':0, 'pierce':False, 'Special':None},
                9:{'Defense':0, 'Attack':10, 'Area Linear':[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], 'Area Diag':[[(1,-1)]], 'delay':0, 'pierce':False, 'Special':None},
                10:{'Defense':0, 'Attack':10, 'Area Linear':[[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)]], 'Area Diag':[[(1,-1)]], 'delay':0, 'pierce':False, 'Special':None}}
#===========================================

#================Abilities==================
# 0:{'Defense':0, 'Attack':3, 'Special':None, 'Area Linear':[(1,2),(1,1),(1,0),(1,-1),(1,-2)], 'Area Diag':[(1,-1)], 'delay':4, 'order linear':[1,1,1,1,1], 'order diag':[1]},
#                 1:{'Defense':0, 'Attack':4, 'Special':None, 'Area Linear':[(1,1),(1,-1),(2,2),(2,-2),(3,3),(3,-3)], 'Area Diag':[(1,-1)], 'delay':20, 'order linear':[2,2,2], 'order diag':[1]},
#                 2:{'Defense':0, 'Attack':5, 'Special':None, 'Area Linear':[(1,1),(1,-1),(1,0),(2,1),(2,-1),(2,0),(3,1),(3,-1),(3,0)], 'Area Diag':[(1,-1)], 'delay':20, 'order linear':[3,3,3], 'order diag':[1]}}
#===========================================
all_equippable_stats = {'chest':chest_stats, 'head':head_stats, 'legs':leg_stats, 'weapon':weapon_stats}
all_name_dict = item_name_dict.copy()
all_name_dict.update(armor_name_dict)
all_name_dict.update(weapon_name_dict)

all_description_dict = item_description_dict.copy()
all_description_dict.update(armor_description_dict)
all_description_dict.update(weapon_description_dict)