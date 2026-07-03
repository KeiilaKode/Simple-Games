class Weapon:
    all_weapons:list = []

    def __init__(self, name:str, kind:str, damage:int, value:int):
        self.name = name
        self.kind = kind
        self.damage = damage
        self.value = value
        Weapon.all_weapons.append(self)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')\n"

    # Need to fix how hero.info() and this __str__ interact
    def __str__(self):
        return (f"{self.name} is a {self.kind}, and does {self.damage} DMG."
                f"It's worth {self.value} $$$")

class Item:
    def __init__(self, name: str, description: str, value: int = 0):
        self.name = name
        self.description = description
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def __str__(self):
        return f"{self.name} - {self.description}"