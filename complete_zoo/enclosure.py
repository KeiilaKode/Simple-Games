from animal import Terrestrial, Aerial, Aquatic

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


# Child Classes Inherits from Building:

### HOUSING FOR THE LAND ANIMALS ###
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
        # SMART CHECK: Is this creature actually a land animal?
        if not isinstance(creature, Terrestrial):
            print(f"Error: {creature.name} is not a land animal and cannot go in {self.name}!")
            return

        if len(self.creatures) < self.max_capacity:
            self.creatures.append(creature)
            self.capacity += 1
        else:
            print(f"{self.name} is full!")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (f" Enclosure: {self.name} |"
                f" Creatures: {len(self.creatures)} |"
                f" Employees: {len(self.assigned_employees)}")


### 2. HOUSING FOR BIRDS ###
class Aerial_Enclosure(Building):
    all_Aerial_Enclosures = []

    def __init__(self, name, wing):
        super().__init__(name=name, wing=wing)
        self.creatures = []
        self.max_capacity = 15  # Maybe aviaries can hold more!
        Aerial_Enclosure.all_Aerial_Enclosures.append(self)

    def add_creature(self, creature):
        # SMART CHECK: Is this creature actually a bird?
        if not isinstance(creature, Aerial):
            print(f"Error: {creature.name} cannot fly and cannot go in {self.name}!")
            return

        if len(self.creatures) < self.max_capacity:
            self.creatures.append(creature)
            self.capacity += 1
        else:
            print(f"{self.name} is full!")

    def __str__(self):
        return f"Aviary: {self.name} | Creatures: {len(self.creatures)} | Employees: {len(self.assigned_employees)}"


### 3. HOUSING FOR WATER ANIMALS ###
class Aquatic_Enclosure(Building):
    all_Aquatic_Enclosures = []

    def __init__(self, name, wing):
        super().__init__(name=name, wing=wing)
        self.creatures = []
        self.max_capacity = 5  # Maybe tanks hold fewer animals
        Aquatic_Enclosure.all_Aquatic_Enclosures.append(self)

    def add_creature(self, creature):
        # SMART CHECK: Is this creature actually a water animal?
        if not isinstance(creature, Aquatic):
            print(f"Error: {creature.name} cannot swim and will drown in {self.name}!")
            return

        if len(self.creatures) < self.max_capacity:
            self.creatures.append(creature)
            self.capacity += 1
        else:
            print(f"{self.name} is full!")

    def __str__(self):
        return f"Aquarium: {self.name} | Creatures: {len(self.creatures)} | Employees: {len(self.assigned_employees)}"




