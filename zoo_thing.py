# A Game in the Terminal about working at a Zoo as Cashier # NOT COMPLETE #

import time

# Tickets
class Ticket:

    def __init__(self, ticket_type):
        self.price = 0
        self.ticket_type = ticket_type
        if self.ticket_type == "Adult":
            self.price = 10
        elif self.ticket_type == "Child":
            self.price = 5

    def __str__(self):
        return f"{self.ticket_type} Ticket: {self.price}."
###########################

# Visitors
class Visitor:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.max_money = 100

        self.impression = 0
        self.impression_max = 10
        self.tickets = []        # The visitor starts with no tickets
        self.amount_spent = 0


    def __str__(self):
        return f"{self.name} spent {self.amount_spent} and has {self.money} dollars left."

    @property
    def has_ticket(self):
        # Returns True if the visitor has at least one ticket in their list
        return len(self.tickets) > 0

    def pay(self, amount):
        # Checks if the visitor has enough money, deducts it, and hands it over
        if self.money >= amount:
            self.money -= amount
            self.amount_spent += amount
            return amount
        else:
            return 0  # Not enough money

##########################

# Employees
class Employee:
    all_employees = []
    def __init__(self, name, job_title, wing=None):
        self.name = name
        self.job_title = job_title
        self.wing = wing
    def __repr__(self):
        return self.__str__
    def __str__(self):
        return f"Employee: {self.name} the {self.job_title} | Area: {self.wing} | "

    def greet(self, visitor):
        print(f"{self.name}: Hello {visitor.name}, my name is {self.name} and I'll be assisting you today!")
    def feed(self, creature):
        pass

# Child class of Employee
class GateKeeper(Employee):

    def __init__(self, name, job_title):
        super().__init__(name=name, job_title=job_title)

        self.register = 0
        # NEW: Trackers for tickets sold
        self.adult_tickets_sold = 0
        self.child_tickets_sold = 0

    def report(self, current_visitors):

        total_tickets = self.adult_tickets_sold + self.child_tickets_sold


        print(f"\n--- Shift Report for {self.name} ---")
        print(
            f"{self.name} has sold {self.adult_tickets_sold} 'Adult' tickets and {self.child_tickets_sold} 'Child' tickets, "
            f"totaling {total_tickets} tickets in all.")
        print(f"Total Money Made: ${self.register}")
        print(f"Current Zoo Capacity: {current_visitors} visitors are inside.")
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
            print(f"{katie.name}: I'm sorry, unfortunately you don't have enough money to enter the zoo."
                  f" Please come back at a later time {visitor.name}.\n")
            print("-" * 33 + "\n")
            return False


#############################################
             ### GAME LOOP ###
#############################################

# --- SIMULATION DRIVER ---

if __name__ == "__main__":
    # 1. Hire your GateKeeper
    katie = GateKeeper(name="Katie", job_title="Gate Keeper")

    print("--- ZOO SIMULATION STARTED ---")
    print("Type 'q' at the name prompt to quit.")
    print("Type 'r' to see amount of tickets sold so far.\n")

    sale_number = 0
    visitors_in_the_zoo = 0

    # 2. The Continuous Loop (Simulating a line of people)
    while True:
        # Generate a visitor dynamically via console input
        print("-" * 33)
        visitor_name = input("Enter the next visitor's name: ").title()

        if visitor_name.lower() == 'r':
            katie.report(visitors_in_the_zoo)
            continue
        elif visitor_name.lower() == 'q':
            print("Closing the zoo gates!")
            break

        visitor_money = int(input(f"How much money does {visitor_name} have? $"))
        print("-" * 33 + "\n")

        # Instantiate the Visitor
        current_visitor = Visitor(name=visitor_name, money=visitor_money)

        print("\n--- Interaction Begins ---")
        # 3. The Interaction
        katie.greet(current_visitor)


        # Ask for ticket counts
        adults = int(input("How many ADULT tickets are needed? "))
        time.sleep(.5)
        kids = int(input("And how many CHILD tickets are needed? "))
        print("\n")
        time.sleep(.5)

        # Process the sale
        transaction_successful = katie.sell_tickets(visitor=current_visitor, num_adults=adults, num_kids=kids)

        # This below, is the same thing as: if transaction_successful == False:
        if not transaction_successful:
            print("-" * 33 + "\n")
            continue

        sale_number += 1
        visitors_in_the_zoo += len(current_visitor.tickets)
        # 4. Check the aftermath to ensure logic worked
        time.sleep(1)
        print("\n*---* Events Happening *---*")
        print(f"*{current_visitor.name} hands {katie.name} the money and then {katie.name} hands them their tickets.*")
        print(f"*They eagerly smile and wave goodbye, making their way into the zoo.*")
        print("-" * 33 + "\n")
        time.sleep(2)
        print("\n--- Transaction Results ---")
        print(f"Completed Sales: {sale_number}")
        print(current_visitor)
        print(f"Tickets purchased: {len(current_visitor.tickets)}")
        print(f"Money in Katie's Register: ${katie.register}")
        print("-" * 33 + "\n")



