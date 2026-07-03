class Zoo:
    def __init__(self, name):
        self.name = name

        # The master lists that hold your entire game's data
        self.buildings = []
        self.enclosures = []
        self.all_employees = []

        self.bank_account = 5000  # You can start tracking total zoo funds!

    def add_building(self, building):
        self.buildings.append(building)

    def add_enclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def hire_employee(self, employee):
        self.all_employees.append(employee)

    # A helper method to easily find an employee by their name
    def get_employee(self, name):
        for employee in self.all_employees:
            if employee.name.lower() == name.lower():
                return employee
        return None