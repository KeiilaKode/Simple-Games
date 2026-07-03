from weapons_stuff import Weapon, Item
from inventory import Store, Bag
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

# ---Treasure Items for the Story ---
crowbar = Item("Crowbar", "A sturdy iron crowbar, good for prying things open.", 5)
treasure_chest = Item("Treasure Chest", "A small, heavy chest. It appears to be locked.", 50)
diving_mask = Item("Diving Mask", "A glass mask with a rubber seal. Allows you to see underwater.", 15)
collar = Item("Collar", "A strange leather collar with a rusted buckle.", 2)
torch = Item("Torch", "A wooden stick with a pitch-soaked rag wrapped around the end.", 3)
glass_bottle = Item("Glass Bottle", "An empty glass bottle. Could hold liquid.", 1)
small_pouch = Item("Small Pouch", "A little leather bag for carrying small things.", 5)
sharpening_stone = Item("Sharpening Stone", "A coarse stone used to keep blades sharp.", 4)
torn_note = Item("Old Note", "...if you manage to gap the hole, you cant miss the place straight ahead..", 0)
treasure_chest_key = Item("Chest Key", "A larger key that looks as if it fits into a chest.", 10)
old_rotted_meat = Item("Rotting Meat", "Its a disgusting rotting piece of meat.", 3)


lil_bag = Bag("Regular Backpack", 10, "Small")
key = Item("Small key", "A small key that looks to little for a chest.", 5)
arrow_head = Item("Arrow Head", "A sharp rock that's been grind down into the shape of an arrow head.", 2)
health_potion = Item("Health Potion", "A potion that restores a portion of your health.", 10)
attack_elixir = Item("Attack Plus", "An elixir that increases your attack damage by 3 for 2 turns.", 15)

diving_snorkel = Item("Diving Snorkel", "", 5)

# Valuable Loot to keep or sell
red_ring = Item("The Red Ring", "A peculiar glowing ring with a red gemstone. It emanates a deep power or energy.", )
blue_ring = Item("The Blue Ring", "A peculiar glowing ring with a blue gemstone. It glistens a beautiful sparkle on the walls.", )
green_ring = Item("The Green Ring", "A peculiar glowing ring with a green gemstone. It seems to make you feel stronger.", )
black_ring = Item("The Black Ring", "A peculiar glowing ring with a black gemstone. You start to forget why you were here.", )


# Characters--NPCs to potentially meet #

# tom = Hero("Tom", "Warrior")
# link = Hero("Link", "Knight")
# case = Hero("Case", "Assassin")
# bridget = Hero("Bridget", "Woman")
# sally = Hero("Sally", "Woman")
# bob = Hero("Bob", "Thug")

# Enemies--NPCs to potentially meet #

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


