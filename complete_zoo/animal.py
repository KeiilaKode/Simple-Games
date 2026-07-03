

# Abstract Parent class Animal
class Animal:
    all_animals = []
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.hunger_lvl = 0
        self.hunger_lvl_max = 10
        self.alive = True
        self.species = self.__class__.__name__
        Animal.all_animals.append(self)
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return f"{self.species} named {self.name}, Age:{self.age}, Hunger:{self.hunger_lvl}"
# Child class Terrestrial from Animal
class Terrestrial(Animal):
    all_terrestrials = []
    def __init__(self, name, age=None):
        super().__init__(name=name, age=age)
        Terrestrial.all_terrestrials.append(self)
# Child class Aquatic from Animal
class Aquatic(Animal):
    all_aquatics = []
    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Aquatic.all_aquatics.append(self)
# Child class Aerial from Animal
class Aerial(Animal):
    all_aerials = []
    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Aerial.all_aerials.append(self)

















