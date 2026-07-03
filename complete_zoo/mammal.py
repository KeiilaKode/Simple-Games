from complete_zoo.animal import Terrestrial
from enclosure import Building

       ### LAND ANIMALS ###

# Abstract Class, Non-Instantiated, Will make around 7 different mammal classes
class Mammal(Terrestrial):
    all_mammals = []

    def __init__(self, name, age):
        super().__init__(name=name)
        self.age = age
        Mammal.all_mammals.append(self)


# 1
# Child Class Lion 4, inherits from Mammal, 3, inherits from Terrestrial, 2, that inherits from Animal, 1
class Lion(Mammal):
    all_lions = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Lion.all_lions.append(self)

# 2
# Child Class Tiger 4, inherits from Mammal, 3, inherits from Terrestrial, 2, that inherits from Animal, 1
class Tiger(Mammal):
    all_tigers = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Tiger.all_tigers.append(self)


# 3
# Child Class Leopard 4, inherits from Mammal, 3, inherits from Terrestrial, 2, that inherits from Animal, 1
class Leopard(Mammal):
    all_leopards = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Leopard.all_leopards.append(self)


# 4
# Child Class Gorilla 4, inherits from Mammal, 3, inherits from Terrestrial, 2, that inherits from Animal, 1
class Gorilla(Mammal):
    all_gorillas = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Gorilla.all_gorillas.append(self)


# 5
# Child Class Chimpanze 4, inherits from Mammal, 3, inherits from Terrestrial, 2, that inherits from Animal, 1
class Chimpanzee(Mammal):
    all_chimpanzee = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Chimpanzee.all_chimpanzee.append(self)


# 6
# Child Class Black_Bear 4, inherits from Mammal, 3, inherits from Terrestrial, 2, that inherits from Animal, 1
class Black_Bear(Mammal):
    all_black_bear = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Black_Bear.all_black_bear.append(self)


# 7
# Child Class Kodiak_Bea 4, inherits from Mammal, 3, inherits from Terrestrial, 2, that inherits from Animal, 1
class Kodiak_Bear(Mammal):
    all_kodiak_bear = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Kodiak_Bear.all_kodiak_bear.append(self)



