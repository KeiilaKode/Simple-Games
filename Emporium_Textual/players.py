from weapons_stuff import *
from inventory import *


class Character:
    all_characters = []

    def __init__(self, name: str, role: str, health: int = 100):
        self.name = name
        self.role = role
        self.health = health
        self.health_max = health

        self.weapon = Weapon("Fists", "Unarmed", 1, 0)
        self.bag = Bag(f"{name}'s bag", 10)
        Character.all_characters.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self):
        return f"{self.name} the {self.role} has ({self.health}/{self.health_max}HP)"

    def get_stats_string(self):
        """Returns a cleanly formatted string for the Textual UI sidebar."""
        return (f"--- {self.name.upper()}'S STATS ---\n"
                f"Class: {self.role}\n"
                f"HP: {self.health}/{self.health_max}\n"
                f"Weapon: {self.weapon.name} ({self.weapon.damage} DMG)\n"
                f"Bag: {len(self.bag.purse)}/{self.bag.capacity} Items")

    def equip(self, weapon_name: str):
        # Search the bag for the weapon by string name
        for item in self.bag.purse:
            if item.name.lower() == weapon_name.lower() and isinstance(item, Weapon):
                self.weapon = item
                return f"*** {self.name} equips the {item.name}! ***"

        return f"*** You don't have a '{weapon_name}' in your bag, or it isn't a weapon. ***"

    def attack(self, target):
        target.health -= self.weapon.damage
        return f"{self.name} attacks {target.name} with the {self.weapon.name} dealing {self.weapon.damage} DMG!"

    def pick_up(self, thing):
        collected = self.bag.add_item(thing)
        if collected:
            return f"*** You picked up the {thing.name} and added it to your inventory. ***"
        else:
            return f"*** Your bag is too full to hold the {thing.name}! ***"

    def get_inventory_string(self):
        """Returns a list of items for the UI."""
        if not self.bag.purse:
            return "*** Your bag is currently empty. ***"

        inv_list = "*** INVENTORY ***\n"
        for item in self.bag.purse:
            inv_list += f"- {item.name}\n"
        return inv_list


class Hero(Character):
    def __init__(self, name, role):
        super().__init__(name=name, role=role)


class Enemy(Character):
    def __init__(self, name, role):
        super().__init__(name=name, role=role)