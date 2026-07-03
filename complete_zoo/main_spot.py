import time
from visitor import Visitor
from zoo_builder import setup_zoo
from animal import Animal
### RUN THE FIRST CHAPTER  * ### * CREATING VISITORS ###
if __name__ == "__main__":
    # 1. Receive the entire loaded zoo
    active_zoo = setup_zoo()

    # 2. Pull Katie out of the zoo's roster so she can run the front gate!
    katie = active_zoo.get_employee("Katie")

    print(f"\n--- {active_zoo.name.upper()} SIMULATION STARTED ---")
    print("Option 1: Type 'q' to quit.")
    print("Option 2: Type 'r' to see the report.")
    print("Option 3: Type 'show' to see the list of current animals at the zoo.")
    print("Option 4: Enter your name.")
    print("-" * 33 + "\n")
    sale_number = 0
    # 2. The Continuous Loop (Simulating a line of people)
    while True:
            # Generate a visitor dynamically via console input
        print("-" * 33)
        visitor_name = input("Enter the next visitor's name: ").title()
        if visitor_name.lower() == 'r':
            katie.report()
            continue
        elif visitor_name.lower() == 'q':
            print("Closing the zoo gates!")
            break

        elif visitor_name.lower() == 'show':
            Animal.show_all()
            continue


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





# 3. Test it out!
# print(katie)
# print(katie.building)
# print(richard)
# print(richard.building)
# print(lions_den.assigned_employees)
# print(enter_center.assigned_employees)