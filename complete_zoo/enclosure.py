# Abstract Parent Class
class Structure:
    def __init__(self, name):
        self.name = name


# Child Class Inherits from Structure
class Building(Structure):
    all_buildings = []

    # Added a default 'wing' here so standard buildings can use it too
    def __init__(self, name, wing="Main Entry"):
        super().__init__(name=name)
        self.capacity = 0
        self.wing = wing

        # MOVED UP: All buildings can now hold employees!
        self.assigned_employees = []

        Building.all_buildings.append(self)

    # MOVED UP: All buildings can now assign employees!
    def assign_employee(self, employee):
        self.assigned_employees.append(employee)
        employee.building = self.name
        employee.wing = self.wing


### HOUSING FOR THE LAND ANIMALS ###

# Child Class Inherits from Building
class Terrestrial_Enclosure(Building):
    all_Terrestrial_Enclosures = []
    mammals = []

    def __init__(self, name, wing):
        # We pass 'name' and 'wing' up to the Building to handle
        super().__init__(name=name, wing=wing)

        # ONLY Enclosures get these attributes
        self.creatures = []
        self.max_capacity = 10

        Terrestrial_Enclosure.all_Terrestrial_Enclosures.append(self)

    # ONLY Enclosures get this method
    def add_creature(self, creature):
        if len(self.creatures) < self.max_capacity:
            self.creatures.append(creature)
            self.capacity += 1
            Terrestrial_Enclosure.mammals.append(creature)
        else:
            print(f"{self.name} is full!")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (f"Enclosure: The {self.name} in the {self.wing} wing | "
                f"Creatures: {len(self.creatures)} | "
                f"Employees: {len(self.assigned_employees)}")




