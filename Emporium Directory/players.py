from weapons_stuff import *
from inventory import *
#from creation_page import fists

class Character:
    all_characters = []
    def __init__(self, name: str, role: str, health: int = 100):
        self.name = name
        self.role = role
        self.health = health
        self.health_max = health

        self.weapon = Weapon("Fists", "Unarmed", 1, 0) # OR change this back to self.weapon = fists, and create the object elsewhere
        self.bag = Bag(f"{name}s bag", 10)
        Character.all_characters.append(self)

    def __repr__(self):
        # When you print the LIST, you only see: [Hero('Link'), Enemy('Ganon')]
        # No health here!
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self):
        # When you print(hero), you see: Link (80/100 HP)
        # This is where the health lives!
        return f"{self.name} the {self.role} has ({self.health}/{self.health_max}HP)"

    def show_stats(self):
        # Unpack the dictionary values into your display strings
        stat_title = f"---CHARACTER ATTRIBUTES---"
        stat_name = f" NAME:  {self.name}"
        stat_role = f" CLASS: {self.role}"
        stat_hp = f" HP:    {self.health}/{self.health_max}"
        stat_weapon = f" WEAPON:{self.weapon.name} ({self.weapon.damage} DMG)"
        stat_bag = f" BAG:   {len(self.bag.purse)}/{self.bag.capacity} Items"

        # Prints it all out in a frame to the terminal.
        print("*^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^*")  # Top Boarders
        print("<" + "'"  * 52 + ">")
        print(f"|{stat_title:^52}|")  # Body with Injected Stats (The :<52 keeps the right wall aligned!)
        print(f"|{stat_name:<52}|")
        print(f"|{stat_role:<52}|")
        print(f"|{stat_hp:<52}|")
        print(f"|{stat_weapon:<52}|")
        print(f"|{stat_bag:<52}|")
        print("<" + "," * 52 + ">")  # Bottom Borders
        print("*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*")




    def equip(self, weapon):
        if weapon in self.bag.purse:
            self.weapon = weapon
            print(f"{self.name} equips the {weapon.name}")
        else:
            print(f"{self.name} doesn't have a {weapon.name} in their bag!")

    def info(self):
        print(f"{self.name} the {self.role}, is wielding the {self.weapon.name}, and has {self.health} out of {self.health_max}HP.")

    def attack(self, target):
        print(f"{self.name} attacks {target.name} with the {self.weapon.name} dealing {self.weapon.damage}DMG")
        target.health -= self.weapon.damage

    def pick_up(self, thing):
        collected = self.bag.add_item(thing)
        if collected:
            print(f"You picked up a {thing.name} and added to your inventory..")

        else:
            print(f"Your {self.bag.name} is too full to hold the {thing.name}!")

    def barter(self):
        pass

class Hero(Character):
    def __init__(self, name, role):
        super().__init__(name=name, role=role)


class Enemy(Character):
    def __init__(self, name, role):
        super().__init__(name=name, role=role)




