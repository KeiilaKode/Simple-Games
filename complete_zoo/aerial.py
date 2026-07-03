from animal import Aerial

# FLYING ANIMALS #

# 1
# Child Class Parrot, inherits from Aerial, inherits from Animal: Will make around 7 different Aerial child classes
class Parrot(Aerial):
    all_parrots = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Parrot.all_parrots.append(self)

# 2
# Child Class Eagle, inherits from Aerial, inherits from Animal
class Eagle(Aerial):
    all_eagles = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Eagle.all_eagles.append(self)

# 3
# Child Class Turkey, inherits from Aerial, inherits from Animal
class Turkey(Aerial):
    all_turkeys = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Turkey.all_turkeys.append(self)

# 4
# Child Class Ostrich, inherits from Aerial, inherits from Animal
class Ostrich(Aerial):
    all_ostriches = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Ostrich.all_ostriches.append(self)

# 5
# Child Class Peacock, inherits from Aerial, inherits from Animal
class Peacock(Aerial):
    all_peacocks = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Peacock.all_peacocks.append(self)

# 6
# Child Class Chicken, inherits from Aerial, inherits from Animal
class Chicken(Aerial):
    all_chickens = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Chicken.all_chickens.append(self)


# 7
# Child Class Falcon, inherits from Aerial, inherits from Animal
class Falcon(Aerial):
    all_falcons = []

    def __init__(self, name, age):
        super().__init__(name=name, age=age)
        Falcon.all_falcons.append(self)




