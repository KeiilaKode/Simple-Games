from ticket import Ticket
import time
# Employees
class Employee:
    all_employees = []
    # We set building=None so you don't HAVE to assign a building on day 1
    def __init__(self, name, job_title, building=None):
        self.name = name
        self.job_title = job_title
        # If a building object is passed, grab its name. Otherwise, say "Unassigned"
        self.building = building.name if building else "Unassigned"
        self.wing = building.wing if building else "Unassigned"
        Employee.all_employees.append(self)
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        # FIXED: This now looks at the employee's own building variable
        return f"Employee: {self.name} the {self.job_title} | Building: {self.building} | Wing: {self.wing}"
    def greet(self, visitor):
        print(f"{self.name}: Hello {visitor.name}, my name is {self.name} and I'll be assisting you today!")
    def feed(self, creature):
        pass
# Child class of Employee
class GateKeeper(Employee):
    def __init__(self, name, job_title, building=None):
        super().__init__(name=name, job_title=job_title, building=building)
        self.register = 0
        self.adult_tickets_sold = 0
        self.child_tickets_sold = 0
        self.visitors_in_the_zoo = 0
    def report(self):
        total_tickets = self.adult_tickets_sold + self.child_tickets_sold
        print(f"\n--- Shift Report for {self.name} ---")
        print(
            f"{self.name} has sold {self.adult_tickets_sold} 'Adult' tickets and {self.child_tickets_sold} 'Child' tickets, "
            f"totaling {total_tickets} tickets in all.")
        print(f"Total Money Made: ${self.register}")
        print(f"Current Zoo Capacity: {self.visitors_in_the_zoo} visitors are inside.")
        print("-" * 33, "\n")




    def sell_tickets(self, visitor, num_adults, num_kids):

        # 1. Calculate the total cost
        total_cost = (num_adults * 10) + (num_kids * 5)
        print(f"{self.name}: Okie dokie, that will be ${total_cost} in all, please.")
        time.sleep(1)

        # 2. Ask the visitor for the money
        money_received = visitor.pay(total_cost)

        # 3. Verify the payment
        if money_received == total_cost:
            # Put money in the building's register (Eventually)
            self.register += money_received
            total_just_bought = num_adults + num_kids
            self.visitors_in_the_zoo += total_just_bought


            # 4. Generate the tickets on the fly and give them to the visitor AND update trackers
            for _ in range(num_adults):
                visitor.tickets.append(Ticket("Adult"))
                self.adult_tickets_sold += 1  # <-- Ticks up by 1

            for _ in range(num_kids):
                visitor.tickets.append(Ticket("Child"))
                self.child_tickets_sold += 1  # <-- Ticks up by 1

            print(f"{self.name}: Thank you, let me get your tickets ready... ah, and here are your {len(visitor.tickets)} tickets.")
            time.sleep(1)
            print(f"Alright well we hope yall have fun and enjoy your time at the zoo!")
            print("-" * 33 + "\n")
            time.sleep(1)
            return True
        else:
            print(f"{self.name}: I'm sorry, unfortunately you don't have enough money to enter the zoo."
                  f" Please come back at a later time {visitor.name}.\n")
            print("-" * 33 + "\n")
            return False


