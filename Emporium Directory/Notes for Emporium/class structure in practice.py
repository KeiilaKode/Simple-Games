# Staff Tracking System

class Employee:
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id

    def __str__(self):
        return f"Employee name: {self.name}: ID Number: {self.employee_id}"

    def __eq__(self, other):
        # if this other object, is the same class as Employee
        if isinstance(other, Employee):
            # where you call the attribute to compare
            return self.employee_id == other.employee_id
        return False

    def __add__(self, other):
        raise ValueError("Can not add Employees!")


class Manager(Employee):
    def __init__(self, name, employee_id, department):
        super().__init__(name, employee_id)

        self.department = department

    def __str__(self):
        return (f"Employee name: {self.name} from the {self.department} "
                f"department: ID Number: {self.employee_id}")

    def __eq__(self, other):
        # if this other object, is the same class as Employee
        if isinstance(other, Manager):
            # where you call the attribute to compare
            return self.department == other.department
        return False

    def __add__(self, other):
        raise ValueError("Can not add Managers!")


class Staff(Employee):
    def __init__(self, name, employee_id, role):
        super().__init__(name, employee_id)
        self.role = role

    def __str__(self):
        return (f"Employee name: {self.name}: ID Number: {self.employee_id}"
                f" Role: {self.role}")

    def __eq__(self, other):
        # if this other object, is the same class as Employee
        if isinstance(other, Staff):
            # where you call the attribute to compare
            return self.role == other.role
        return False

    def __add__(self, other):
        raise ValueError("Can not add Staff!")


# Employees
p1 = Employee("Josh", "004")
p2 = Employee("Tim", "001")

# Managers
m1 = Manager("Trish", "002", "roof")
m2 = Manager("Markie", "081", "roof")

# Staff
s1 = Staff("Ben", "091", "old timer")
s2 = Staff("John", "0991", "new fish")
# print(p1,p2)
# print(m1,m2)
# print(s1, s2)

print(m1 == m2)
#print(s1 + s2)