from animal import Aquatic
# WATER ANIMALS
# 1
# Abstract Child Class Fish, inherits from Aquatic, inherits from Animal: Will make around 7 different Aerial child classes
class Fish(Aquatic):
    all_fish = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Fish.all_fish.append(self)

# 2
# Child Class Octopus, inherits from Aquatic, inherits from Animal
class Octopus(Aquatic):
    all_octopus = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Octopus.all_octopus.append(self)

# 3
# Child Class Squid, inherits from Aquatic, inherits from Animal
class Squid(Aquatic):
    all_squid = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Squid.all_squid.append(self)

# 4
# Child Class Sea_Urchin, inherits from Aquatic, inherits from Animal
class Sea_Urchin(Aquatic):
    all_sea_urchin = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Sea_Urchin.all_sea_urchin.append(self)

# 5
# Child Class Shark, inherits from Aquatic, inherits from Animal
class Shark(Aquatic):
    all_shark = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Shark.all_shark.append(self)

# 6
# Child Class Dolphin, inherits from Aquatic, inherits from Animal
class Dolphin(Aquatic):
    all_dolphin = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Dolphin.all_dolphin.append(self)

# 7
# Child Class Star_fish, inherits from Aquatic, inherits from Animal
class Star_fish(Aquatic):
    all_star_fish = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Star_fish.all_star_fish.append(self)