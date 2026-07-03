from weapons_stuff import Weapon
from players import Character, Hero, Enemy


# Weapons

fists = Weapon("Fists", "Unarmed", 1, 0)
knife = Weapon("Knife", "One-handed", 1, 2)

# One-handed/Two-handed
mace = Weapon("Mace", "Blunt", 3, 4)
axe = Weapon("Axe", "Two-handed", 3, 4)
iron_sword = Weapon("Iron Sword", "One-handed", 4, 5)
claymore = Weapon("Claymore", "One-handed", 6, 5)

# Ranged
short_bow = Weapon("Short Bow", "Ranged", 3, 6)
Long_bow = Weapon("Long Bow", "Ranged", 5, 8)
cross_bow = Weapon("Cross Bow", "Ranged", 7, 10)

# Magical Ranged
wand = Weapon("Wand", "Magical", 4, 7)
staff = Weapon("Staff", "Magical", 5, 10)

# Characters
# tom = Hero("Tom", "Warrior")
# link = Hero("Link", "Knight")
# case = Hero("Case", "Assassin")
# bridget = Hero("Bridget", "Woman")
# sally = Hero("Sally", "Woman")

# Enemies
# slime = Enemy("Slime", "Environmental Hazard")
# waylon = Enemy("Waylon", "Wizard")
# brunt = Enemy("Brutus", "Enforcer")
# chris = Enemy("Chris", "Bitch")
# gremlin = Enemy("Grimm", "Monster")
# gremlin_1 = Enemy("Grim-ly", "Monster")
# gremlin_2 = Enemy("Grim-by", "Monster")
# gremlin_3 = Enemy("Grim-ster", "Monster")
# gremlin_4 = Enemy("Grim-ber", "Monster")
# gremlin_5 = Enemy("Grim-bim", "Monster")
# gremlin_6 = Enemy("Grim-mer", "Monster")


# Actions
# hero.attack(enemy)
# hero.equip(iron_sword)
# hero.attack(enemy)
# good.info()
# bad.info()
# good.attack(bad)
# bad.info()
# enemy.info()
# print(Weapon.weapons)

tom = Hero("Tom", "Warrior")
bob = Hero("Bob", "Thug")
# print(bob)
# print(Character.all_characters)
bob.equip(knife)